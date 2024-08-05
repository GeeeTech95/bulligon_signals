from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.urls import reverse

from .serializers import UserSerializer, LoginSerializer, DetailVerificationSerializer
from Users.models import Notification




class Register(generics.CreateAPIView):
    permission_classes = []
    authentication_classes = []
    model = get_user_model()
    serializer_class = UserSerializer
    ref_id = None


    def add_referral(self,ref_id,user):

        if ref_id:
            # add for user
            try:
                referee = self.model.objects.get(referral_id=ref_id)
                user.referee = referee
                # save and create parameters
                # notify user of bonus
                msg = "{} just registered with you referal id".format(
                    self.user.nick_name)
                Notification.objects.create(user=referee, message=msg)
                user.save()
            except:
                pass
      



    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(
            data=request.POST, context={"request": request})
        if serializer.is_valid():
            user = serializer.save()
            self.add_referral(serializer.validated_data.get('referral_id'),user)

            # log user in
            login(request, user)

            # redirect to details verification
            return Response(
                {"success_url": reverse("verify-email")}
            )

        else:
            print(serializer.errors)
            return Response(
                serializer.errors,
                status=400
            )


class Login(generics.CreateAPIView):
    permission_classes = []
    authentication_classes = []
    model = get_user_model()
    serializer_class = LoginSerializer

    def get_success_url(self):
        user = self.request.user
        if not user.email_verified:
            url = reverse("verify-email")

        elif not user.phone_number_verified:
            url = reverse("verify-phone-number")

        else:
            url = reverse("dashboard")
        return url

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            email = data.get("email")
            password = data.get("password")

            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                auth_token, created = Token.objects.get_or_create(user=user)

                return Response(
                    {
                        "auth_token": auth_token.key,
                        "success_url": self.get_success_url()
                    }
                )

            else:
                return Response(
                    {"detail": "authentication failed, please enter the correct credentials"},
                    status=400
                )

        else:
            return Response(
                serializer.errors,
                status=400
            )


class DetailVerification(generics.GenericAPIView):
    serializer_class = DetailVerificationSerializer

    def get_success_url(self, ver_type):
        user = self.request.user
        # if email was just verified take us to phone number and so
        if ver_type == "email":
            # check if phone number has been verified
            if not user.phone_number_verified:
                return reverse("verify-phone-number")

        elif ver_type == "phone_number":
            # check if email has been verified
            if not user.email_verified:
                return reverse("verify-email")

        return reverse("dashboard")

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            ver_type = serializer.validated_data['verification_type']
            return Response(
                {"success_url": self.get_success_url(ver_type)}
            )

        else:
            return Response(
                serializer.errors,
                status=400
            )
