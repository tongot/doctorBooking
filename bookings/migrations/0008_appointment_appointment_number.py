# Generated by Django 3.0.3 on 2020-02-24 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0007_patient_medical_aid_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='appointment_number',
            field=models.CharField(default='0000', max_length=4, unique=True),
        ),
    ]
