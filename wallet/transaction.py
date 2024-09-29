from django.shortcuts import render
from django.views.generic import ListView, View, RedirectView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from urllib.parse import urlparse, urlunparse, urljoin
from .models import Wallet,  Plan, PendingDeposit
from .forms import DepositForm, SubscriptionForm
from Users.models import Notification
from myadmin.models import Settings as AdminSetting
from core.communication import TransactionMail
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
import datetime



class Deposit(LoginRequiredMixin, View):
    template_name = 'deposit.html'
    form_class = DepositForm
    model = PendingDeposit

    def get(self, request, *args, **kwargs):
        # if self.model.objects.filter(user= request.user,is_active = True).exists():
        # return HttpResponse("You still have a pending deposit, please wait for approval")
        form = self.form_class
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
     
        # if self.model.objects.filter(user= request.user,is_active = True).exists():
        # return HttpResponse("You still have a pending deposit, please wait for approval")

        form = self.form_class(request.POST, request.FILES)
        user = request.user
        response = {}
        if form.is_valid():
            form.save(commit=False)
            msg = "Your ${} deposit transaction has been registered and is being processed, you will be notified when processing is completed.".format(
                form.cleaned_data['amount']
            )

            form.instance.user = user
            deposit = form.save()
            messages.success(request, msg)

            response['success_url'] = reverse('dashboard')
            response['success'] = True
            return JsonResponse(response)

        else:
            print('helo')
            print(form.errors)
            response['form_errors'] = form.errors.as_ul()
            return JsonResponse(response)


class Plans(LoginRequiredMixin, ListView):
    template_name = 'plans.html'
    model = Plan
    context_object_name = "plans"


class Subscribe(LoginRequiredMixin, View):
    template_name = 'subscribe.html'
    form_class = SubscriptionForm
    model = Plan
    plan = None

    def get_context(self):
        ctx = {}
        user_balance = self.request.user.user_wallet.available_balance
        # check if balance will permit
        if user_balance < self.plan.cost:
            ctx['low_balance'] = True

        # max should be user balance of plan max, which ever is larger
        ctx['max_amount'] = min(self.plan.cost or 0.00, user_balance)
        ctx['default_cost'] = min(self.plan.cost, user_balance)
        ctx['plan'] = self.plan
        return ctx

    def get(self, request, *args, **kwargs):
        # check if user has pending deposit
        _slug = kwargs.get('slug', None)
        if not _slug:
            return HttpResponse("Invalid request")
        try:
            self.plan = self.model.objects.get(slug=_slug)
        except self.model.DoesNotExist:
            return HttpResponse("Plan you selected does not exist")
        ctx = self.get_context()
        ctx['form'] = self.form_class

        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        _slug = kwargs.get('slug', None)
        if not _slug:
            return HttpResponse("Invalid request")
        try:
            self.plan = self.model.objects.get(slug=_slug)
        except self.model.DoesNotExist:
            return HttpResponse("Plan you selected does not exist")
        form = self.form_class(user=request.user, data=request.POST)

        if form.is_valid():
            user = request.user
            form.save(commit=False)
            form.instance.user = user
            subscription = form.save()
         

            # default
            msg = "You have succesfully subscribed to the {} subscription plan (pending processing), with an initial capital of ${}".format(
                form.instance.plan.name,
                form.cleaned_data['amount']
            )

            if not subscription.approve_subscriptions():
                if user.user_wallet.allow_automatic_subscription:
                    subscription.on_approve()
                   
                   
                    msg = "You have succesfully subscribed to the {} subscription plan, with an initial capital of ${}".format(
                        form.instance.plan.name,
                        form.cleaned_data['amount']
                    )

            messages.success(request, msg)
            # send mail

            return HttpResponseRedirect(reverse('dashboard'))
        else:

            ctx = self.get_context()
            ctx['form'] = form

            return render(request, self.template_name, ctx)


