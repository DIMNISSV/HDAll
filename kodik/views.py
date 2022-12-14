from django.http import JsonResponse, HttpResponse
from django.shortcuts import render




def panel_view(request):
    return render(request, 'kodik/panel.html', context={})
