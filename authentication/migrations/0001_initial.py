# Generated by Django 4.1.7 on 2023-03-05 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFirebaseUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('firebase_uid', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True, verbose_name='Firebase User ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email Address')),
                ('first_name', models.CharField(max_length=30, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Last Name')),
                ('phone_number', models.CharField(max_length=15, unique=True, verbose_name='Phone Number')),
                ('signed_up', models.DateTimeField(verbose_name='Signed Up')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='Last Login')),
                ('last_activity', models.DateTimeField(blank=True, null=True, verbose_name='Last Activity')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Custom Firebase User',
                'verbose_name_plural': 'Custom Firebase Users',
            },
        ),
    ]
