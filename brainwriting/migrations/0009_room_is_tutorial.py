# Generated by Django 3.0.5 on 2020-06-05 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brainwriting', '0008_auto_20200602_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_tutorial',
            field=models.BooleanField(default=False),
        ),
    ]