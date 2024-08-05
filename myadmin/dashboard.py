from django.views.generic import View,TemplateView,ListView,DetailView
from django.views.generic.edit import  DeleteView,UpdateView
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.shortcuts import render 
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.db.models  import Sum

from wallet.models import PendingDeposit, Transaction
from .models import Settings as ModelSetting
from .forms import SettingsForm
from django.utils import timezone
from django.contrib.auth import get_user_model

class AdminBase(UserPassesTestMixin,LoginRequiredMixin,) :

    def get_user(self) :
        return None
    
    def test_func(self) : 
        return self.request.user.is_staff or self.request.user.is_superuser


class Dashboard(AdminBase,View) :
    template_name = 'admin-dashboard.html'
    tx_model = Transaction

    def get(self,request,*args,**kwargs) :
        transaction_history = Transaction.objects.all().order_by('-date')[:8]
        site_revenue = self.tx_model.objects.filter(
            transaction_type = "DEPOSIT",
            status = "Approved"
        ).aggregate(
            revenue = Sum("amount")
        )['revenue'] or 0.00
        registered_users = get_user_model().objects.all().count()
        return render(request,self.template_name,locals())    


class Settings(AdminBase,View) :
    model = ModelSetting
    form_class = SettingsForm
    template_name = "form.html"

    def get(self,request,*args,**kwargs) :
        form = self.form_class(initial=self.model.objects.all()[0].__dict__)
        form_title = "Admin Settings"
        return render(request,self.template_name,locals())

    def post(self,request,*args,**kwargs) :  
        form = self.form_class(request.POST) 
        if form.is_valid() :
            first_obj = self.model.objects.all()[0]
            for field in form.fields.keys() :
                try : setattr(first_obj,field,form.cleaned_data.get(field))
                except TypeError : continue
            first_obj.save() 
            return HttpResponseRedirect(reverse('admin-dashboard'))
        else :
            return render(request,self.template_name,locals())




