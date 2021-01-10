from django.db import models
from users.models import QuermiProfileUser

SUBSCRIPTION_MODE_STATUS = [
    ('MONTHLY', 'Monthly'),
    ('YEARLY', 'Yearly'),
]
DESC_LENGTH = 512


class PaymentRegister(models.Model):
    profile = models.ForeignKey(
        QuermiProfileUser,
        related_name='payment_method', on_delete=models.CASCADE)
    payment_id = models.TextField(unique=True)
    last_four_digits_card = models.TextField(max_length=4)
    exp_month = models.TextField()
    exp_year = models.TextField()
    card_type = models.TextField()


class SubscriptionMode(models.Model):
    subscription_id = models.TextField()
    name = models.TextField()
    description = models.TextField(max_length=DESC_LENGTH, blank=True)
    price = models.IntegerField()
    mode = models.TextField(choices=SUBSCRIPTION_MODE_STATUS)

    def __str__(self):
        return self.name


class SubscriptionRegister(models.Model):
    sub_payment_id = models.TextField(unique=True)
    profile = models.OneToOneField(
        QuermiProfileUser, on_delete=models.CASCADE)
