
from urllib import request
from django.shortcuts import render
from django.views.generic import ListView,View,RedirectView,TemplateView
from django.views.generic.edit import CreateView,UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .models import Settings
from .forms import SettingForm


class UpdateSetting(LoginRequiredMixin,UpdateView) :
    template_name = 'settings.html'
    password_form = PasswordChangeForm
    form_class = SettingForm
    model = Settings

    def get(self,request,*args,**kwargs) :
        password_form = self.password_form(request.user)
        setting_form =  self.form_class
        sett_active = "active"
        return render(request,self.template_name,locals())
    
      

    def post(self,request,*args,**kwargs):
        password_form = self.password_form(self.request.user)
        setting_form =  self.form_class
        form = self.form_class(request.POST)
        if form.is_valid() :
            user = request.user
            for field in form.fields.keys() :
                value = form.cleaned_data.get(field)
                #change on/off to True or false
                try : setattr(user.settings,field,value)
                except TypeError : continue
                user.settings.save()
            messages.success(self.request,"Your settings was updated successfully.") 
            return HttpResponseRedirect(reverse('dashboard'))

        else :
            password_form = self.password_form(request.user)
            return render(request,self.template_name,locals())


    def get_object(self) :
        return self.request.user



class UpdatePassword(LoginRequiredMixin,UpdateView) :
    template_name = 'settings.html'
    form_class = PasswordChangeForm
    setting_form = SettingForm
 

    def get_object(self) :
        return self.request.user

    
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.user,request.POST)
        if form.is_valid() :
            user = form.save()
            update_session_auth_hash(request,user)   #Very Important
        else :
            password_form = form
            setting_form =  self.setting_form
            return render(request,self.template_name,locals())    
        messages.success(self.request,"Your password was updated successfully.") 
        return HttpResponseRedirect(reverse('dashboard'))
    

