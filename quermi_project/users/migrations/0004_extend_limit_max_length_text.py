# Generated by Django 3.0.8 on 2020-08-09 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_add_subfields_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quermiprofileuser',
            name='experience',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='quermiprofileuser',
            name='profile_description',
            field=models.TextField(max_length=255),
        ),
    ]
