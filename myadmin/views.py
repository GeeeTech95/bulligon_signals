from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import TemplateView



class TOS(TemplateView) :
    template_name = "tos.html"
