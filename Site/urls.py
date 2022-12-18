from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

from Site import settings

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('post/', include('post.urls')),
    path('account/', include('account.urls')),
    path('video/', include('video.urls')),
    path('search/', include('search.urls')),
    path('oreder_table/', include('order_table.urls')),
    path('kodik/', include('kodik.urls')),
    path('97905f0ebd3eb55b94a0e70660b9059d.txt/', lambda r: HttpResponse('97905f0ebd3eb55b94a0e70660b9059d'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    