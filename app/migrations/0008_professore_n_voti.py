# Generated by Django 3.0.7 on 2020-06-19 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20200607_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='professore',
            name='n_voti',
            field=models.IntegerField(default=0),
        ),
    ]