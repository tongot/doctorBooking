# Generated by Django 3.0.3 on 2020-02-19 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_restrictedbookingdates'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='bookedfor',
            field=models.CharField(default='willard', max_length=400),
        ),
    ]
