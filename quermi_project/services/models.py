from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import QuermiProfileUser

CONTRACT_STATUS = [
    ('CPEN', 'Pending contact'),
    ('CADD', 'Contact added'),
    ('CACT', 'Actived contract'),
    ('CDFT', 'Defeated contract'),
]
L_MAX_LENGTH = 512
MIN_RATE = 1
MAX_RATE = 5


class Contract(models.Model):
    patient = models.ForeignKey(
        QuermiProfileUser, related_name='patient', on_delete=models.CASCADE)
    care_person = models.ForeignKey(
        QuermiProfileUser, related_name='care_person',
        on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    status = models.TextField(choices=CONTRACT_STATUS)

    def __str__(self):
        return 'contract - {from_p} - {to_p}'.format(
            from_p=self.care_person,
            to_p=self.patient
        )


class Report(models.Model):
    date = models.DateTimeField(auto_now=True)
    description = models.TextField(
        max_length=L_MAX_LENGTH, blank=True, null=True)
    rate = models.IntegerField(validators=[
        MinValueValidator(MIN_RATE),
        MaxValueValidator(MAX_RATE)
    ])
    origin_profile = models.ForeignKey(
        QuermiProfileUser,
        on_delete=models.CASCADE, related_name='origin_profile')
    profile_rated = models.ForeignKey(
        QuermiProfileUser,
        on_delete=models.CASCADE, related_name='profile_rated')
