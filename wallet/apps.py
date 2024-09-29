from django.apps import AppConfig
from django.core.signals import request_finished




class WalletConfig(AppConfig):
    name = 'wallet'
 
    def ready(self) :
        from . import signals
        from .models import Transaction,Subscription,PendingDeposit
        request_finished.connect(signals.transaction_handler, sender=Transaction) 
        request_finished.connect(signals.subscription_handler, sender=Subscription)
        request_finished.connect(signals.deposit_handler, sender=PendingDeposit)      
