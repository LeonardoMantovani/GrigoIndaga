# Generated by Django 3.0.7 on 2020-06-07 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_votazione_nome_prof'),
    ]

    operations = [
        migrations.AddField(
            model_name='professore',
            name='metodo',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='professore',
            name='preparazione',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='professore',
            name='rapporto',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='professore',
            name='spiegazione',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='professore',
            name='valutazioni',
            field=models.IntegerField(default=0),
        ),
    ]