from .views import LoginRedirect
from django.urls import path,include
from . import views,security


urlpatterns = [

    path('login-redirect/',LoginRedirect.as_view(),name = 'login-redirect'),
    path("test-template/",views.TestTemplate.as_view(),name = "test-template"),
    path('security/send-code', security.SendCode.as_view(),
         name='send-code')
]