
from django.shortcuts import render
from django.views.generic import ListView, View, RedirectView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from core.communication import AccountMail
from .forms import ProfileForm, VerifyEmailForm, WalletForm

from core.communication import AccountMail
from core.forms import OtpForm


class Profile(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    model = get_user_model()
    form_class = ProfileForm
    wallet_form = WalletForm
    verify_email_form = VerifyEmailForm
    otp_form = OtpForm

    def get_success_url(self):
        messages.success(
            self.request, "Your profile was updated successfully.")
        return reverse('dashboard')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        ctx = super(Profile, self).get_context_data(**kwargs)
        ctx['wallet_form'] = self.wallet_form(
            initial=model_to_dict(self.request.user))
        ctx['verify_email_form'] = self.verify_email_form(
            initial=model_to_dict(self.request.user))
        ctx['otp_form'] = self.otp_form
        ctx['tab'] = self.request.GET.get('tab', 'personal-data')
        ctx['prof_active'] = "active"
        return ctx


class WalletUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    model = get_user_model()
    form_class = WalletForm

    def get_success_url(self):
        messages.success(
            self.request, "Your wallet details was updated successfully.")
        return reverse('dashboard')

    def get_object(self):
        return self.request.user


class VerifyEmail(LoginRequiredMixin, View):
    template_name = 'verify-email.html'
    form_class = VerifyEmailForm
    otp_form = OtpForm

    def get(self, request, *args, **kwargs):
        if request.user.email_verified :
            msg = "Your email has already been verified."
            messages.success(request,msg)
            return HttpResponseRedirect(reverse("dashboard"))
        mail = AccountMail(request.user)
        mail.send_verification_code()
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):

        response = {}
        otp = request.POST.get('otp')
        try:
            otp = int(otp)
        except:
            response['error'] = "The code you entered is invalid or has expired. please request for another one."
            return JsonResponse(response)
        # send mail
        msg = "Your email has been verified successfully ."
        if request.user.security.validate_otc(otp):
            self.request.user.email_verified = True
            self.request.user.save()
            response['success'] = True
            messages.success(request,msg)

        else:
            response['error'] = "The code you entered is not valid or has expired. please request for another one."



        if request.user.email_verified:
            messages.success(msg)
            mail = AccountMail(send_type='support')
            mail.send_generic_email('Email Verified successfully', msg)

        return JsonResponse(response)
