from django.urls import path, include

from . import profile, account


urlpatterns = [

    # ACCOUNTS
    path("account/register/", account.Register.as_view(), name='register-api'),
    path("account/login/", account.Login.as_view(), name='login-api'),

    # VERIFICATION
    path("account/verify-details/", account.DetailVerification.as_view(),
         name="verify-details-api"),

    # PROFILE
    path("profile/update/", profile.UpdateProfile.as_view(), name="update-profile"),


]
