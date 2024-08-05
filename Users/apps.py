from django.apps import AppConfig
from django.core.signals import request_finished
from django.contrib.auth import get_user_model


class UsersConfig(AppConfig):
    name = 'Users'

    def ready(self) :
        from . import signals
        request_finished.connect(signals.create_user_related, sender=get_user_model())    


