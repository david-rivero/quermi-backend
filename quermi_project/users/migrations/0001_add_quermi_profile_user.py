# Generated by Django 3.0.8 on 2020-07-07 23:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuermiProfileUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=30)),
                ('rate', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('profile_description', models.TextField(max_length=120)),
                ('birth_date', models.DateTimeField()),
                ('available_hour_from', models.TimeField()),
                ('available_hour_to', models.TimeField()),
                ('languages', models.TextField(choices=[('ES', 'Spanish'), ('EN', 'English')])),
                ('services', models.TextField(choices=[('HCR', 'Home caring'), ('MOR', 'Market orders'), ('WKR', 'Walk around'), ('PRO', 'Procedures'), ('PHY', 'Pharmacy'), ('HCL', 'Home cleaning'), ('SFC', 'Self caring'), ('OTH', 'Other')])),
                ('experience', models.CharField(max_length=120)),
                ('address', models.CharField(max_length=50)),
            ],
        ),
    ]
