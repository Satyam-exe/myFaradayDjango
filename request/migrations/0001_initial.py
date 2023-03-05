# Generated by Django 4.1.7 on 2023-03-05 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestModel',
            fields=[
                ('request_id', models.IntegerField(editable=False, primary_key=True, serialize=False, verbose_name='Request ID')),
                ('time_of_request', models.DateTimeField(verbose_name='Time of Request')),
                ('name', models.CharField(max_length=100, verbose_name='Full Name')),
                ('address', models.CharField(max_length=100, verbose_name='Address')),
                ('city', models.CharField(max_length=50, verbose_name='City')),
                ('state', models.CharField(max_length=50, verbose_name='State/Territory')),
                ('country', models.CharField(max_length=2, verbose_name='Country')),
                ('pincode', models.CharField(max_length=6, verbose_name='Postal Code')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email Address')),
                ('phone_number', models.CharField(max_length=15, unique=True, verbose_name='Phone Number')),
                ('longitude', models.DecimalField(blank=True, decimal_places=15, max_digits=18, null=True, verbose_name='Longitude')),
                ('latitude', models.DecimalField(blank=True, decimal_places=15, max_digits=18, null=True, verbose_name='Latitude')),
                ('firebase_uid', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='profiles.profile', verbose_name='Firebase User ID')),
            ],
            options={
                'verbose_name': 'Request',
                'verbose_name_plural': 'Requests',
            },
        ),
    ]