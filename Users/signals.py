from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Settings, Security,KYC
from wallet.models import Wallet

from core.communication import AccountMail


@receiver(post_save, sender=get_user_model())
def create_user_related(sender, instance, created, **kwargs):

    if created:

        Wallet.objects.create(user=instance)
        Settings.objects.create(user=instance)
        Security.objects.create(user=instance)
        #KYC.objects.create(user=instance)
        #send mail
        mail = AccountMail(instance)
        mail.send_registration_email()

        if instance.referee :
            mail.send_referral_mail()


