from django.shortcuts import render
from django.views.generic import View, RedirectView
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse


class LoginRedirect(RedirectView):
    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_admin:
                return HttpResponseRedirect(reverse('admin-dashboard'))
            else:
                return HttpResponseRedirect(reverse('dashboard'))
        except:
            return HttpResponseRedirect(reverse('dashboard'))


class TestTemplate(TemplateView):
    template_name = "403.html"  #registration/registration-mail.html

    def get_context_data(self, **kwargs):
        from Users.models import User
        ctx = super(TestTemplate, self).get_context_data(**kwargs)
        ctx['instance'] = User.objects.first()
        return ctx


def error_404_handler(request, exception):
    template_name = "404.html"
    return render(request, template_name, locals())


def error_500_handler(request):
    template_name = "500.html"
    return render(request, template_name, locals())


def error_403_handler(request, exception):
    template_name = "403.html"
    return render(request, template_name, locals())
