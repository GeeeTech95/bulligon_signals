from  django.urls import path,include
from .views import Subscribe
from .accounts import Register,LoginRedirect
from .dashboard import KYC, Dashboard, Referral,Transaction
from .profile import Profile, WalletUpdate,VerifyEmail
from .settings import UpdatePassword, UpdateSetting



urlpatterns = [
    #ACCOUNT
    path('subscribe/',Subscribe.as_view(),name = 'subscribe'),
    path('register/',Register.as_view(),name = 'register'),
   


    #PROFILE 
    path('profile/',Profile.as_view(),name = 'profile'),
    path('profile/verify-email/',VerifyEmail.as_view(),name = 'verify-email'),
    path('profile/update-wallet/',WalletUpdate.as_view(),name = 'wallet_update'),

    #SETTINGS
    path('settings/',UpdateSetting.as_view(),name = 'setting'),
    path('settings/update-password/',UpdatePassword.as_view(),name = 'update-password'),

    #DASHBOARD
    path('dashboard/',Dashboard.as_view(),name = 'dashboard'),

    path('kyc/',KYC.as_view(),name = 'kyc'),
    path('settings/',UpdateSetting.as_view(),name = 'setting'),
    path('transactions/',Transaction.as_view(),name = 'transaction'),
    path('referral/',Referral.as_view(),name = 'referral'),
    path('login-redirect/',LoginRedirect.as_view(),name="login-redirect")




]