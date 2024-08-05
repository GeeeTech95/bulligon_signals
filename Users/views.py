from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from .forms import SubscribeForm
from .models import NewsLaterSubscriber

class Subscribe(View) :
    form_class = SubscribeForm
    model = NewsLaterSubscriber
    def post(self,request,*args,**kwargs) :
        feedback = {}
        form = self.form_class(request.POST)
        if form.is_valid() :
            form.save()
            feedback['success'] = 'subscribed'
        else : feedback['error'] = form.errors['email']    
        return JsonResponse(feedback)
