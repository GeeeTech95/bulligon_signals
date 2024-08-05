
from django.shortcuts import render
from django.views.generic import RedirectView, View
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
# import imgkit
from io import BytesIO
# from  xhtml2pdf import pisa
import random
# from twilio.rest import Client
from django.core.mail import EmailMultiAlternatives, SafeMIMEMultipart
from email.mime.image import MIMEImage

from core.templatetags.vocabulary import capitalize
import os


class TransactionMail():

    def __init__(self, instance):
        self.instance = instance
        self.mail = Email("transaction")

    def send_transaction_mail(self):
        template_name = "transaction/transaction-mail.html"

        self.mail.send_html_email(
            [self.instance.user.email],
            template_name,
            subject="Transaction Confirmation on {}".format(
                settings.SITE_NAME),
            ctx={"transaction": self.instance}
        )

    def send_withdrawal_application_mail(self):
        msg = "Your ${} withdrawal application has been submitted for processing, You will be notified once completed.".format(
            self.instance.amount)
        template_name = "transaction/withdrawal-application-mail.html"
        self.mail.send_html_email(
            [self.instance.user.email],
            template_name,
            subject=" Your Withdrawal Request on {}".format(
                settings.SITE_NAME),
            ctx={"instance": self.instance}
        )

    def send_deposit_mail(self):
        # handle for created and approved

        template_name = "transaction/pending-deposit-mail.html"
        self.mail.send_html_email(
            [self.instance.user.email],
            template_name,
            subject="Your Deposit Request on {} is Awaiting Network Confirmations".format(
                settings.SITE_NAME),
            ctx={"instance": self.instance}
        )

    def send_investment_mail(self):

        template_name = "transaction/investment-mail.html"
        self.mail.send_html_email(
            [self.instance.user.email],
            template_name,
            subject="Your Investment on {} Has Been Processed Successfully".format(
                capitalize(settings.SITE_NAME)),
            ctx={"instance": self.instance}
        )


class AccountMail():
    def __init__(self, user):
        self.user = user

    def send_generic_email(self, subject, text):
        mail = Email("support")
        mail.send_html_email(
            [self.user.email],
            template="email/generic-mail.html",

            ctx={"text": text, "name": self.user.name}
        )

    def send_registration_email(self):
        mail = Email("support")

        mail.send_html_email(
            [self.user.email],
            template="email/registration/registration-mail.html",
            subject="Welcome to {}! Your Journey into Crypto Investment Starts ".format(
                settings.SITE_NAME),
            ctx={"name": self.user.name}
        )

    def send_referral_mail(self):

        self.mail.send_html_email(
            [self.instance.referee.email],
            "email/registration/referral-mail.html",
            subject="Congratulations! You've Earned a Referral Bonus on {} 🎉".format(
                settings.SITE_NAME),
            ctx={"instance": self.instance}
        )

    def send_verification_code(self):
        code_validity = 10  # minutes
        otc = random.randrange(127054, 924979)
        self.user.security.otc = otc
        self.user.security.otc_expiry = timezone.now(
        ) + timezone.timedelta(minutes=code_validity)
        self.user.security.save()
        mail = Email("security")
        mail.send_html_email(
            [self.user.email],
            template="email/security/verification-code-mail.html",
            subject="{} One Time Code".format(settings.SITE_NAME),
            ctx={"code": otc, "verification_code_validity": code_validity}
        )


class Email():
    def __init__(self, send_type="support"):

        from django.core.mail import get_connection

        host = settings.EMAIL_HOST
        port = settings.EMAIL_PORT
        password = settings.EMAIL_HOST_PASSWORD

        senders = {
            'support': settings.EMAIL_HOST_USER_SUPPORT,
            "security": settings.EMAIL_HOST_USER_SUPPORT,
            "transaction": settings.EMAIL_HOST_USER_TRANSACTION,
        }

        if not send_type:
            self.send_from = senders['support']

        else:
            self.send_from = senders.get(send_type, senders['support'])

        self.auth_connecion = get_connection(
            host=host,
            port=port,
            username=self.send_from,
            password=password,
            use_tls=settings.EMAIL_USE_TLS
        )

    def send_email(self, receive_email_list, subject, message, headers=None):
        headers = {
            'Content-Type': 'text/plain'
        }
        try:
            email = EmailMessage(subject=subject, body=message,
                                 from_email=self.send_from, to=receive_email_list,
                                 headers=headers, connection=self.auth_connecion)
            email.send()
            self.auth_connecion.close()
        except:
            pass

    def send_html_email(self, receive_email_list, template=None, subject=None, files_path_list=None, ctx=None):
        error = None  # for error control
        subject = subject or self.default_subject
        template = template or self.default_template
        ctx = ctx
        ctx['site_name'] = settings.SITE_NAME
        msg = render_to_string(template, ctx)

        email = EmailMultiAlternatives(
            subject,
            msg,
            self.send_from,
            receive_email_list,
            connection=self.auth_connecion
        )
        email.content_subtype = "html"
        email.mixed_subtype = "related"

        BASE_DIR = settings.STATIC_URL
        logo_path = os.path.join(
            settings.BASE_DIR, "static/main/images/logo/logo-dark.png")
        with open(logo_path, 'rb') as f:
            logo = MIMEImage(f.read())
            logo.add_header("Content-ID", "<logo.png>")
            email.attach(logo)

        """if isinstance(files_path_list,list) :
            for file in files_path_list :
                "fetch image"
                with open(file,"rb") as f :
                    image = MIMEImage(f.read())"""
        """with open(logo_path, mode='rb') as f :
            image = MIMEImage(f.read())
            email.attach(image)
            image.add_header('Content-ID',"<logo>") """

        # if settings.DEBUG : print(msg)
        try:
            email.send()
        except:
            error = "mail was not sent successfully"
            print(error)
        self.auth_connecion.close()

        return error

    def send_file_email(self, file_name, _file, receive_email_list, subject, message):
        email = EmailMessage(subject, message, self.send_from,
                             receive_email_list, connection=self.auth_connecion)
        email.attach(file_name, _file)
        try:
            email.send()
            self.auth_connecion.close()
        except:
            pass
