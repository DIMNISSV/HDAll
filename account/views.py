from django.contrib.auth import get_user_model

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.crypto import md5
from django.utils.datetime_safe import datetime
from django.views import generic

from Site import settings
from main.mixins import BaseMixin
from . import models, forms, utils


class RegistrationView(generic.CreateView, BaseMixin):
    title = 'Регистрация'
    form_class = forms.RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration.html'


class ProfileView(generic.DetailView, BaseMixin):
    model = get_user_model()
    template_name = 'registration/profile.html'
    context_object_name = 'user'

    def get_object(self, **kwargs):
        self.title = self.title = f'Просмотр пользователя {self.request.user.username}'
        current = self.request.user.username
        username = self.kwargs.get('username', current)
        return get_object_or_404(get_user_model(), username=username)


class ProfileEdit(generic.UpdateView, LoginRequiredMixin, BaseMixin):
    model = get_user_model()
    template_name = 'registration/edit.html'
    context_object_name = 'user'
    fields = ['username', 'email', 'first_name', 'last_name', 'birth_date', 'dark_theme', 'page_size']

    def get_pk(self):
        self.title = f'Редактирование пользователя {self.request.user.username}'
        return self.request.user.pk

    def get(self, *args, **kwargs):
        self.kwargs['pk'] = self.get_pk()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.kwargs['pk'] = self.get_pk()
        return super().post(*args, **kwargs)


class SubscribeView(generic.ListView, LoginRequiredMixin, BaseMixin):
    model = models.Subscribe
    context_object_name = 'subscribes'
    template_name = 'registration/subscribe.html'

    def get_context_data(self, **kwargs):
        if self.kwargs.get('subscribe'):
            subscribe = get_object_or_404(models.Subscribe, title=self.kwargs.get('subscribe'))
            periods = {
                1: subscribe.price * 1., 3: subscribe.price * 3 * .95,
                6: subscribe.price * 6 * .90, 12: subscribe.price * 12 * .85
            }
            kwargs['subscribe'] = subscribe
            kwargs['periods'] = periods.items()
            if self.kwargs.get('period'):
                amount = periods[self.kwargs.get("period")]
                checked = _check_subscribe(self.request, subscribe)
                if checked[0]:
                    transaction = models.Transaction.objects.create(user=self.request.user, amount=amount,
                                                                    period=self.kwargs.get("period"),
                                                                    subscribe=subscribe)
                    transaction.save()
                    sign = _gen_sign(amount, transaction.pk)
                    if amount == 0:
                        kwargs['link'] = f'{reverse_lazy("subscribe_complete")}' \
                                         f'?amount=0&sign={sign}&MERCHANT_ORDER_ID={transaction.pk}'
                    else:
                        kwargs['link'] = \
                            f'https://pay.freekassa.ru/?m={settings.FREEKASSA_M}&oa={periods[self.kwargs.get("period")]}' \
                            f'&currency={settings.FREEKASSA_CURRENCY}&o={transaction.pk}' \
                            f'&em={self.request.user.email}&s={sign}'
                kwargs['msg'] = checked[1]
        context = super().get_context_data(**kwargs)
        self.title = f'Обновление подписки {self.request.user.username}'
        return context


def subscribe_complete_view(request):
    transaction = models.Transaction.objects.get(pk=request.GET.get('MERCHANT_ORDER_ID'))
    sign = _gen_sign(transaction.amount, transaction.pk)
    user = _get_user(transaction.user_id)
    if sign != request.GET.get('sign'):
        return HttpResponse('Ошибка подписи!')
    elif user != request.user:
        return HttpResponse('Ошибка пользователя!')
    user.subscribe_id = transaction.subscribe_id
    m = transaction.period
    now = datetime.now()
    if datetime(user.subscribe_to.year, user.subscribe_to.month,
                user.subscribe_to.day) < now or user.subscribe.price < transaction.subscribe.price:
        c_y = now.year
        c_m = now.month
        c_d = now.day
    else:
        c_y = user.subscribe_to.year
        c_m = user.subscribe_to.month
        c_d = user.subscribe_to.day
    c_m, c_y = utils.get_month(c_m, c_y, m)
    user.subscribe_to = datetime(c_y, c_m, c_d, user.subscribe_to.hour,
                                 user.subscribe_to.minute, tzinfo=timezone.utc)
    user.save()
    return redirect('main_page')


def _check_subscribe(request, subscribe):
    user = _get_user(request.user.pk)
    current_price = user.subscribe.price if user.subscribe else 0
    true = (True, '')
    if current_price > subscribe.price:
        return False, 'Ваша текущая подписка лучше чем выбранная, подождите пока истечет текущая и обновите потом.'
    elif current_price == subscribe.price:
        if user.subscribe:
            return True, f'Продление подписки. Сейчас ваша истечет {user.subscribe_to}'
        else:
            return true
    else:
        return true


def _get_user(pk):
    return get_user_model().objects.get(pk=pk)


def _gen_sign(amount, t_pk):
    s = f'{settings.FREEKASSA_M}:{float(amount)}:{settings.FREEKASSA_SECRET}:{settings.FREEKASSA_CURRENCY}:{t_pk}'
    sign = md5(
        s
        .encode()).hexdigest()
    return sign
