from django.urls import path, include
from .pages import Index, TOS, About, Contact, Plans,PrivacyPolicy,CookiePolicy


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about-us'),
    path('contact/', Contact.as_view(), name='contact'),
    path('plans/', Plans.as_view(), name='plans'),
    path('privacy-policy/',PrivacyPolicy.as_view(),name='privacy-policy'),
    path('terms-of-service/',TOS.as_view(),name = 'tos'),
    path('cookie-policy/',CookiePolicy.as_view(),name = 'cookie-policy'),

]
