from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Site import settings

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('post/', include('post.urls')),
    path('account/', include('account.urls')),
    path('video/', include('video.urls')),
    path('search/', include('search.urls')),
    path('oreder_table/', include('order_table.urls')),
    path('kodik/', include('kodik.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
