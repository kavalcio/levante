# Generated by Django 3.0.5 on 2020-05-13 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brainwriting', '0003_response_developed'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='voted',
            field=models.IntegerField(default=0),
        ),
    ]