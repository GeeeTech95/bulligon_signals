from django.views.generic import View,TemplateView,ListView,DetailView
from django.views.generic.edit import  DeleteView,UpdateView
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.shortcuts import render
from .dashboard import AdminBase
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model

from .forms import UpdateMemberForm


class FundMember() :
    template_name = "fund-member.html"


class Members(AdminBase,View) :
    template_name = 'members.html'
    model = get_user_model()

    def get(self,request,*args,**kwargs) :
        members = self.model.objects.exclude(
            user_wallet__isnull = True
        ).order_by('-date_joined')
        return render(request,self.template_name,locals())




class MemberDetail(AdminBase,View)  :
    template_name = 'member-profile.html' 
    model = get_user_model()
    context_object_name = "member"
    form_class = UpdateMemberForm
 

    def get(self,request,*args,**kwargs) :
        _pk = kwargs.get('pk',None) 
        if not _pk : return HttpResponse("invalid request")
        try : _user = self.model.objects.get(pk = _pk)
        except : return HttpResponse("User does not exist")
        total_earning = _user.user_wallet.total_past_earning
        initial = {
            "balance" : _user.user_wallet.initial_balance,
            "name" : _user.name,
            "referral_earning" : _user.user_wallet.referral_earning,
            "withdrawal_allowed" : _user.user_wallet.withdrawal_allowed ,
            "allow_automatic_investment" : _user.user_wallet.allow_automatic_investment
        }
        form = self.form_class(initial=initial)
        try : active_investments = _user.investment.filter(is_active = True)
        except : active_investments = None
        member = _user
        return render(request,self.template_name,locals())


    def post(self,request,*args,**kwargs) :
        _pk = kwargs.get('pk',None) 
        if not _pk : return HttpResponse("invalid request")
        try : _user = self.model.objects.get(pk = _pk)
        except : return HttpResponse("User does not exist")
        form = self.form_class(request.POST)

        if form.is_valid() :
            name  = form.cleaned_data.get("name",_user.name)   
            balance = form.cleaned_data.get("balance",_user.user_wallet.initial_balance)   
            referral_earning = form.cleaned_data.get("referral_earning",_user.user_wallet.referral_earning)   
            withdrawal_allowed = form.cleaned_data.get("withdrawal_allowed",_user.user_wallet.withdrawal_allowed)   
            allow_automatic_investment = form.cleaned_data.get("allow_automatic_investment",_user.user_wallet.allow_automatic_investment)

            _user.name = name
            _user.save()
            user_wallet = _user.user_wallet
            user_wallet.initial_balance = balance
            user_wallet.referral_earning = referral_earning
            user_wallet.withdrawal_allowed = withdrawal_allowed
            user_wallet.allow_automatic_investment = allow_automatic_investment
            
            user_wallet.save()

        else :
            initial = {
            "balance" : _user.user_wallet.initial_balance,
            "name" : _user.name,
            "referral_earning" : _user.user_wallet.referral_earning,
            "withdrawal_allowed" : _user.user_wallet.withdrawal_allowed

            }
            form = self.form_class(initial=initial)
            total_earning = _user.user_wallet.current_balance
            return render(request,self.template_name,locals())

        return HttpResponseRedirect(reverse("my-members"))     



class MemberEdit(UpdateView) :

    template_name = 'user-update.html'


class EmailMember() :
    template_name = 'create_email.html'






