# Generated by Django 3.1 on 2020-09-06 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='status',
            field=models.TextField(choices=[('CADD', 'Contact added'), ('CACT', 'Actived contract'), ('CDFT', 'Defeated contract')]),
        ),
    ]
