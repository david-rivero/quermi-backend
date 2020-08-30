from django.db import models
from django.contrib.auth.models import User


class Contract(models.Model):
    patient = models.ForeignKey(
        User, related_name='patient', on_delete=models.CASCADE)
    care_person = models.ForeignKey(
        User, related_name='care_person', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    status = models.TextField()
