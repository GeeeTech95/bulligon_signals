
from django.shortcuts import render
from django.views.generic import ListView, View, RedirectView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.forms.models import model_to_dict
from wallet.models import Subscription, Wallet, Transaction as TR
from django.db.models import Sum
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from .forms import KYCForm


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(Dashboard, self).get_context_data(*args, **kwargs)
        try:
            ctx['pending_deposit'] = self.request.user.user_pending_deposit.all().aggregate(
                total=Sum("amount")
            )['total']
        except:
            pass
    
        ctx['recent_transactions'] = TR.objects.filter(
            user=self.request.user)[:6]

        ctx['time_now'] = timezone.now()
        ctx['dash_active'] = 'active'
        return ctx

    def get_crypto_price_notification(self):
        import requests

        alerting_url = 'https://api.cryptocurrencyalerting.com/v1/alert-conditions'
        alerting_headers = {
            'Authorization': 'Token e1kw1WoNHbT0dogNm9gmW0RDqKniK1y',
            'Content-Type': 'application/json'
        }

        payload = {
            "identity": {"external_id": str(self.request.user.pk)},
            "subscriptions": [
                {
                    "type": "ChromePush",
                    "token": "MTI1OTdmZDctMjA0ZC00ODZiLTgxYmMtOTRjZDFjZjAzODY0"
                }
            ]
        }

        push_url = "https://api.onesignal.com/apps/8bf9716f-f42c-4617-aea1-3c42e57a83b2/users"
        push_headers = {
            "Authorization": "Token MTI1OTdmZDctMjA0ZC00ODZiLTgxYmMtOTRjZDFjZjAzODY0",
            "accept": "application/json",
            "content-type": "application/json"
        }

        response = requests.post(push_url, headers=push_headers, json=payload)

        print(response.text)

        if response.status_code == 200:
            print('Success:', response.json())
        else:
            print('Failed:', response.status_code, response.text)

    def get(self, request, *args, **kwargs):
        # self.get_crypto_price_notification()
        user = request.user
        #user.handle_due_subscriptions()
        # if request.user.user_wallet.plan_is_active and request.user.user_wallet.plan_is_due :
        # request.user.user_wallet.on_plan_complete()

        return render(request, self.template_name, self.get_context_data())


class Transaction(LoginRequiredMixin, ListView):
    model = TR
    template_name = 'user-transactions.html'
    context_object_name = "transactions"

    def get_context_data(self, *args, **kwargs):
        ctx = super(Transaction, self).get_context_data(*args, **kwargs)

        ctx['trans_active'] = 'active'
        return ctx

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class KYC(LoginRequiredMixin, View):
    template_name = "kyc.html"
    form_class = KYCForm

    def get(self, request, *args, **kwargs):
        kyc_active = "active"

        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):

        response = {}

        msg = "Your kyc request has been submitted, review in progress."


        if request.user.is_kyc_verified :
                    response[
                        'error'] = """You have already completed your KYC Verfiication"""
                    return JsonResponse(response)
           
        if request.user.is_kyc_submitted :
                    response[
                        'error'] = """ You have already submitted a KYC application, please wait while our team reviews your application."""
                    return JsonResponse(response)

        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            user = request.user
            form.save(commit=False)
            form.instance.user = user
            form.save()
          
            messages.success(request, msg)
          
            response['success'] = reverse("dashboard")
            return JsonResponse(response)

        else:

            response['form_errors'] = form.errors.as_ul()
            return JsonResponse(response)


       




class Referral (LoginRequiredMixin, TemplateView):

    template_name = 'referral.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        prepend = "https://" if self.request.is_secure() else "http://"
        host = prepend + self.request.get_host()
        ctx['referral_link'] = "{}{}?ref_id={}".format(
            host, reverse("register"), self.request.user.referral_id)
        ctx['ref_active'] = "active"
        return ctx
