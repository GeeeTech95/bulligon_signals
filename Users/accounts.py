from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.views.generic import CreateView, View, RedirectView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from wallet.models import Wallet
from myadmin.models import MyAdmin
from core.notification import Notification
from .models import Settings, User
from .forms import UserCreateForm


class Register(CreateView):
    template_name = 'register.html'
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        initials = {}
        referral_id = None
        if 'ref_id' in request.GET:
            ref_id = request.GET['ref_id']
            try:
                ref_id = int(ref_id)  # cleaning
                referral_id = ref_id
                initials['referral_id'] = ref_id
            except:
                pass

        #form = self.form_class(initial=initials)
        return render(request, self.template_name, locals())

    def add_referral(self):
        ref_id = self.ref_id

        if ref_id:
            # add for user
            try:
                referee = User.objects.get(referral_id=ref_id)
                self.user.referee = referee
                # save and create parameters
                # notify user of bonus
                msg = "{} just registered with you referal id".format(
                    self.user.nick_name)
                Notification.objects.create(user=referee, message=msg)
            except:
                pass
        self.user.save()

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():
            self.ref_id = form.cleaned_data.get('referral_id', None)
            self.user = form.save(commit=False)
            self.add_referral()

       
        else:
            return render(request, self.template_name, locals())
        return JsonResponse({"success_url": self.success_url})


class LoginRedirect(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        if request.user.is_admin:
            return HttpResponseRedirect((reverse('admin-dashboard')))
        else:
            return HttpResponseRedirect((reverse('dashboard')))
