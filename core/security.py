
from django.conf import settings
from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from django.core.validators import validate_email
import random
from Users.models import Security


from .communication import AccountMail


    
class SendCode(LoginRequiredMixin, View):
   
    
    def get(self, request, *args, **kwargs):
        feedback = {}
        mail = AccountMail(request.user)
        mail.send_verification_code()
        feedback['success'] = 'Your verification code has been sent successfully, please check your email account'

        return JsonResponse(feedback)
