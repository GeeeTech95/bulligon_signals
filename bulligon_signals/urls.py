
from django.contrib import admin
from django.urls import path,include
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('site-admin-access/', admin.site.urls),
    path('',include('company.urls')),
    path('',include('core.urls')),
    path('',include('Users.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('signal-wallet/',include('wallet.urls')),
    path('my-admin/',include('myadmin.urls')),

    path('api/v1/',include("Users.api.v1.urls")),
]


if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)



handler404 = 'core.views.error_404_handler'
handler500 = 'core.views.error_500_handler'
handler403 = 'core.views.error_403_handler'