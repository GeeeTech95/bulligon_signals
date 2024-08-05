from email.policy import default
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
import random
import os
from itertools import chain
from django.conf import settings

from core.exceptions import IncorrectPinError
from .managers import UserManager


import os
import random


class Country(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=20)

    def __str__(self):
        return "{}({})".format(self.name, self.short_name)


class User(AbstractBaseUser, PermissionsMixin):
    wallet_choices = (
        ("BTC", "BTC"),
        ("ETH", "ETH"),
        ("USDT", "USDT"),
        ("LTC", "LTC")
    )

    def get_path(instance, filename):
        filename = "{}.{}".format(instance.name, filename.split('.')[1])
        return "users/dp/{}".format(filename)

    def get_path(instance, filename):
        ext = filename.split('.')[1]
        file = "dp.{}".format(ext)
        return "users/profile/{}/{}".format(instance, file)

    username = None
    email = models.EmailField('email address', unique=True)
    account_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    slug = models.SlugField()

    otp = models.CharField(max_length=10, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    picture = models.FileField(upload_to=get_path)
    referee = models.ForeignKey(
        'self', blank=True, null=True, related_name="referral", on_delete=models.SET_NULL)
    referral_id = models.CharField(max_length=30, blank=True, editable=False)

    is_admin = models.BooleanField(default=False)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    # payment wallet
    _wallet_name = models.CharField(
        max_length=10, null=True, choices=wallet_choices)
    _wallet_address = models.CharField(
        max_length=100, null=True, help_text="BEP20 address")

    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        # specify fields to monitor
        self.__fields_to_watch_for_changes = ['email', "phone_number"]
        # set the old values
        for field in self.__fields_to_watch_for_changes:
            setattr(self, '__initial_{}'.format(field), getattr(self, field))

    def has_changed(self, field):
        original = "__initial_{}".format(field)
        return getattr(self, original) != getattr(self, field)
    
    @property
    def is_kyc_verified(self) :
        try : return  self.kyc.filter(status = "approved").exists
        except : return False
        
    @property
    def is_kyc_submitted(self) :
        try : return  self.kyc.exclude(status = "approved").exists 
        except : return False
        
    @property
    def withdrawal_wallet_name(self):
        return self._wallet_name

    @property
    def withdrawal_wallet_address(self):
        return self._wallet_address

    def handle_due_investments(self):
        due_investments = self.investment.filter(
            is_active=True,
            plan_end__lte=timezone.now()
        )

        for investment in due_investments:
            investment.on_plan_complete()

    @property
    def unique_id(self):
        return "BVID{}".format(self.pk)

    @property
    def get_picture(self):
        BASE_DIR = settings.STATIC_URL
        default_path = os.path.join(
            BASE_DIR, "user-dashboard/images/user-thumb-sm.png")
        if not self.picture:
            return default_path

        return self.picture.url

    @property
    def wallet_address_valid(self):
        if not self._wallet_address or not self._wallet_name:
            return False
        return True

    @property
    def active_investments(self):
        
        invs = self.investment.filter(
            is_active=True,
            is_approved=True
        )
        
        return invs

    @property
    def nick_name(self):
        return slugify(self.name)

    def has_changed(self, field):
        original = "__initial_{}".format(field)
        return getattr(self, original) == getattr(self, field)

    def __str__(self):
        return self.name

    @property
    def email_hidden(self):
        email = self.email
        name, extension = email.split("@")
        cut = len(name) - 2
        if cut < 2:
            cut = 2
        if cut > 3:
            cut = 3

        return "{}***@{}".format(name[:3], extension)

    def save(self, *args, **kwargs):

        # check if email changed
        if self.has_changed('email'):
            self.email_verified = False
        self.slug = slugify(self.name)
        if not self.referral_id:
            self.referral_id = random.randrange(999999, 99999999999)
        super(User, self).save(*args, **kwargs)

    class Meta():
        ordering = ['-date_joined']


class Security(models.Model):
    default_trx_pin = "0000"

    def get_transaction_pin_default():
        return make_password("0000")

    user = models.OneToOneField(
        get_user_model(), related_name='security', on_delete=models.CASCADE)
    otc = models.PositiveIntegerField(blank=True, null=True)
    otc_expiry = models.DateTimeField(blank=True, null=True)

    transaction_pin = models.CharField(
        max_length=100, default=get_transaction_pin_default)

    @property
    def otc_expiry_tz_aware(self):
        return timezone.make_aware(self.otc_expiry, timezone.get_default_timezone())

    def __str__(self):
        return self.user.name

    def validate_otc(self, otc):
        if otc != self.otc:
            return False

        if timezone.now() > self.otc_expiry:
            return False

        return True

    def save(self, *args, **kwargs):
        super(Security, self).save(*args, **kwargs)

    def change_transaction_pin(self, old_pin, new_pin):
        # convert old pin to hash
        old_pin = make_password(old_pin)
        if not check_password(new_pin, old_pin):
            raise IncorrectPinError()

        self.transaction_pin = make_password(new_pin)
        self.save()

    def is_transaction_pin_valid(self, pin):
        return check_password(pin, self.transaction_pin)

    def is_transaction_pin_still_default(self):
        return check_password(self.default_trx_pin, self.transaction_pin)

    def __str__(self):
        return self.user.__str__()


class Settings(models.Model):
    user = models.OneToOneField(
        get_user_model(), related_name='settings', on_delete=models.CASCADE)
    email_on_transaction = models.BooleanField(default=True)
    password_on_withdrawal = models.BooleanField(default=True)

    def __str__(self):
        return "{}-setting".format(self.user.nick_name)


class WalletAddress(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="wallet_address", on_delete=models.CASCADE)
    btc_address = models.CharField(max_length=60)
    usdt_address = models.CharField(max_length=60)
    eth_address = models.CharField(max_length=60)


class KYC(models.Model):
    DocTypeChoices = (
        ("Utility Bill","Utility Bill"),
        ("Bank Statement","Bank Statement"),
 
    )

    KYCStatusChoices = (
        ("created","created"),
        ("processing","processing"),
        ("approved","approved"),
        ("denied","denied"),

    

    )
    def get_kyc_upload_path(instance, filename):
        filename = "{}.{}".format(instance.user, filename.split('.')[1])
        return "users/{}kyc/{}".format(instance.user.pk, filename)
   
    user = models.ForeignKey(
        get_user_model(), related_name='kyc', on_delete=models.CASCADE)
    status = models.CharField(max_length=10,choices=KYCStatusChoices,default="created")
    face_capture = models.FileField(upload_to=get_kyc_upload_path)
    id_upload = models.FileField(upload_to=get_kyc_upload_path)
    proof_of_address_type = models.CharField(max_length=20,choices=DocTypeChoices)
    proof_of_address = models.FileField(upload_to=get_kyc_upload_path)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return "{}-KYC-{}".format(self.user,self.date)


class Notification(models.Model):
    user = models.ForeignKey(
        User, related_name='notification', on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta():
        ordering = ['-date']


class NewsLaterSubscriber(models.Model):
    user = models.ForeignKey(
        User, related_name='news_subscibers', on_delete=models.CASCADE)

    def __str__(self):
        return self.email
