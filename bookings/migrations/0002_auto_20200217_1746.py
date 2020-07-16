# Generated by Django 3.0.3 on 2020-02-17 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dependencies',
            name='date_of_registry',
            field=models.DateTimeField(auto_now_add=True, default='2020-02-02', verbose_name='date registry'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dependencies',
            name='gender',
            field=models.CharField(choices=[('M', 'MALE'), ('F', 'FEMALE')], default='M', max_length=1),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('Awaiting', 'Awaiting'), ('Completed', 'Completed')], default='Awaiting', max_length=20),
        ),
    ]
