from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

from payments.utils import create_payment_customer

MIN_VALUE_PROFILE_RATING = 0
MAX_VALUE_PROFILE_RATING = 5
S_MAX_LENGTH = 30
M_MAX_LENGTH = 50
ML_MAX_LENGTH = 100
L_MAX_LENGTH = 255
XXL_MAX_LENGTH = 1024
QUERMI_ROLE = [
    ('PATIENT', 'Patient'),
    ('CARE_PROVIDER', 'Care Provider')
]
QUERMI_SERVICES = [
    ('HCR', 'Home caring'),
    ('MOR', 'Market orders'),
    ('WKR', 'Walk around'),
    ('PRO', 'Procedures'),
    ('PHY', 'Pharmacy'),
    ('HCL', 'Home cleaning'),
    ('SFC', 'Self caring'),
    ('OTH', 'Other')
]
QUERMI_LANG = [
    ('ES', 'Spanish'),
    ('EN', 'English')
]


class ProfileServices(models.Model):
    name = models.TextField(
        choices=QUERMI_SERVICES, unique=True)

    def __str__(self):
        return '{} - {}'.format(self.name, self.pk)


class ProfileLanguage(models.Model):
    name = models.TextField(
        choices=QUERMI_LANG, unique=True)

    def __str__(self):
        return '{} - {}'.format(self.name, self.pk)


class QuermiProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.TextField(max_length=S_MAX_LENGTH, choices=QUERMI_ROLE)
    profile_photo_url = models.TextField(
        max_length=XXL_MAX_LENGTH, null=True)
    doc_id_photo_url = models.TextField(
        max_length=ML_MAX_LENGTH, null=True)
    profile_description = models.TextField(max_length=L_MAX_LENGTH)
    birth_date = models.DateTimeField()
    available_hour_from = models.TimeField()
    available_hour_to = models.TimeField()
    languages = models.ManyToManyField(ProfileLanguage)
    services = models.ManyToManyField(ProfileServices)
    experience = models.CharField(max_length=L_MAX_LENGTH)
    address = models.CharField(
        max_length=M_MAX_LENGTH, null=True, blank=True)
    profile_status = models.JSONField(max_length=ML_MAX_LENGTH, default=dict)
    customer_payment_id = models.TextField(
        max_length=M_MAX_LENGTH, null=True)
    verified_profile = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk and not self.customer_payment_id:
            customer = create_payment_customer()
            self.customer_payment_id = customer.get('id')
        super(QuermiProfileUser, self).save(*args, **kwargs)

    def __str__(self):
        return 'Profile {role} - {st_name} {last_name} - pk: {pk}'.format(
            role=self.role,
            st_name=self.user.first_name,
            last_name=self.user.last_name,
            pk=self.pk
        )

    @property
    def rate(self):
        rate_base = 5
        amount = 0
        for row in self.profile_rated.iterator():
            amount += row.rate

        if not amount:
            return rate_base

        return int(amount / self.profile_rated.count())
