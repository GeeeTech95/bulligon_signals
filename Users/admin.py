from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(Country)
admin.site.register(NewsLaterSubscriber)
admin.site.register(Settings)
admin.site.register(Security)
admin.site.register(KYC)



