from django.urls import reverse_lazy,reverse
from django.shortcuts import render
from django.views.generic import CreateView,View,RedirectView
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from core.notification import Notification
from Users.models import  User
from .forms import UserCreateForm
from .models import Settings,MyAdmin,Subscription
from .forms import SubscribeForm

class Register(CreateView) :
    template_name = 'register.html'
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('login')

    def get(self,request,*args,**kwargs) :
        initials = {}
        form = self.form_class(initial=initials)   
        return render(request,self.template_name,locals())


    def auto_create_myadmin(self,user) :
        model = MyAdmin
        admin = model.objects.create(user = user)
        Settings.objects.create(admin = admin) 
        return

    def post(self,request,*args,**kwargs) :
        form = self.form_class(request.POST)
        if form.is_valid() :
            form.save(commit = False)
            form.instance.is_admin = True
            user  = form.save()
            self.auto_create_myadmin(user)
            msg  = 'Congratulations,Welcome to {},Your admin account was created successfully,You are on a {} days free plan'.format(settings.SITE_NAME,settings.FREE_PLAN_DURATION)
            Notification.notify(user,msg)   
            #send email
            # #send message    
        return HttpResponseRedirect(self.success_url)



class Subscribe(View) :
    template_name = "admin-subscribe.html"
    form_class = SubscribeForm
    
    def get(self,request,*args,**kwargs) :
        form = self.form_class
        return render(request,self.template_name,locals())


class SubscriptionComplete(View) :
    model = Subscription

    def get(self,request,*args,**kwargs) :
        feedback = {}
        if self.model.objects.filter(admin = request.user.user_admin,is_approved = False).exists() :
            feedback['error'] = "You already have a pending subscription awaiting approval"
        model.objects.create(admin = request.user.user_admin)
        feedback['success'] = "Your request was submited successfully,you will be notified upon validation"
        return JsonResponse(feedback)
     


