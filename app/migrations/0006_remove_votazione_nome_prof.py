# Generated by Django 3.0.7 on 2020-06-07 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_votazione'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='votazione',
            name='nome_prof',
        ),
    ]
