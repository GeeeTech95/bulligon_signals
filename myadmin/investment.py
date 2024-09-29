from django.views.generic import CreateView, View, TemplateView, ListView, DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.conf import settings

from wallet.models import Subscription, Plan, Transaction, PendingDeposit
from Users.models import Notification
from .dashboard import AdminBase
import uuid


class CreatePlan(AdminBase, CreateView):
    model = Plan
    success_url = reverse_lazy('plans-admin')
    template_name = 'form.html'
    fields = ['name', 'min_cost', 'max_cost', 'interest_rate', 'duration']

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.admin = self.request.user.user_admin
        form.save()
        return HttpResponseRedirect(self.success_url)


class AllPlans(AdminBase, ListView):
    model = Plan
    template_name = 'plan-list.html'
    context_object_name = "plans"

    def get_queryset(self):
        return self.model.objects.filter(admin=self.request.user.user_admin)


class DepositNotice(AdminBase, ListView):
    model = PendingDeposit
    template_name = 'deposit-notice.html'
    context_object_name = "deposits"

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class ApproveDeposit(AdminBase, View):
    model = PendingDeposit

    def on_approved_deposit(self, instance):
        instance.on_approve()

        # notify user
        msg = "Your ${} deposit has been approved.".format(instance.amount)
        Notification.objects.create(user=instance.user, message=msg)

        # create transaction
        transact = Transaction.objects.create(user=instance.user,
                                              status="Approved",
                                              amount=instance.amount,
                                              transaction_type='DEPOSIT',
                                              coin=instance.payment_method,
                                              description="Deposit Approved"
                                              )

        return

    def get(self, request, *args, **kwargs):
        feedback = {}
        pk = request.GET.get('pk', None)
        if not pk:
            feedback['error'] = "Incomplete request Parameters"
            return JsonResponse(feedback)
        try:
            pd = self.model.objects.get(pk=pk)
            self.on_approved_deposit(pd)
            feedback['success'] = True

            return JsonResponse(feedback)

        except self.model.DoesNotExist:
            feedback['error'] = "this deposit does no longer exist"
            return JsonResponse(feedback)


class DeclineDeposit(AdminBase, View):
    pass



class SubscriptionNotice(AdminBase, ListView):
    model = Subscription
    template_name = 'subscription-notice.html'
    context_object_name = 'subscriptions'

    def get_queryset(self):
        return self.model.objects.exclude(is_approved=True).order_by('-date')


class ApproveSubscription(View):
    model = Subscription

    def on_approved_subscription(self):
        pi = self.pending_subscription
        instance = pi.on_approve()
        # notify user
        msg = "Your ${} subscription has been processed successfully.".format(
            instance.amount)
        Notification.objects.create(user=instance.user, message=msg)
        return

    def get(self, request, *args, **kwargs):
        feedback = {}
        pk = request.GET.get('pk', None)
        if not pk:
            feedback['error'] = "Incomplete request Parameters"
            return JsonResponse(feedback)
        try:

            pending_subscription = self.model.objects.get(pk=pk)
            if pending_subscription.is_approved:
                feedback['error'] = "This transaction has already been processed"
                return JsonResponse(feedback)
            self.pending_subscription = pending_subscription
            self.on_approved_subscription()
            feedback['success'] = True

            return JsonResponse(feedback)

        except self.model.DoesNotExist:
            feedback['error'] = "this subscription no longer exist"
            return JsonResponse(feedback)
