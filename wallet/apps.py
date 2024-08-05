from django.apps import AppConfig
from django.core.signals import request_finished




class WalletConfig(AppConfig):
    name = 'wallet'
 
    def ready(self) :
        from . import signals
        from .models import WithdrawalApplication,Transaction,Investment,PendingDeposit
        request_finished.connect(signals.transaction_handler, sender=Transaction) 
        request_finished.connect(signals.withdrawal_handler, sender=WithdrawalApplication)    
        request_finished.connect(signals.investment_handler, sender=Investment)
        request_finished.connect(signals.deposit_handler, sender=PendingDeposit)      
