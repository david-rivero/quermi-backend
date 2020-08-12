from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

MIN_VALUE_PROFILE_RATING = 0
MAX_VALUE_PROFILE_RATING = 5
S_MAX_LENGTH = 30
M_MAX_LENGTH = 50
L_MAX_LENGTH = 255
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


# Should replace the default User model 
# or mantain profile information in another model?
class QuermiProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.TextField(max_length=S_MAX_LENGTH, choices=QUERMI_ROLE)
    rate = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(MIN_VALUE_PROFILE_RATING),
            MaxValueValidator(MAX_VALUE_PROFILE_RATING)
        ]
    )
    profile_description = models.TextField(max_length=L_MAX_LENGTH)
    birth_date = models.DateTimeField()
    available_hour_from = models.TimeField()
    available_hour_to = models.TimeField()
    languages = models.ManyToManyField(ProfileLanguage)
    services = models.ManyToManyField(ProfileServices)
    experience = models.CharField(max_length=L_MAX_LENGTH)
    address = models.CharField(max_length=M_MAX_LENGTH, null=True)

    def __str__(self):
        return 'Profile {st_name} {last_name} - pk: {pk}'.format(
            st_name=self.user.first_name,
            last_name=self.user.last_name,
            pk=self.pk
        )
