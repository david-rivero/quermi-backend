# Generated by Django 3.1 on 2020-09-11 01:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0002_add_choices_status_field_contract'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, max_length=512, null=True)),
                ('rate', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('origin_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origin_profile', to=settings.AUTH_USER_MODEL)),
                ('profile_rated', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_rated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
