# Generated by Django 4.1.7 on 2023-03-25 09:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('wid', models.BigAutoField(db_column='wid', primary_key=True, serialize=False, verbose_name='Worker ID')),
                ('aadhar_number', models.PositiveBigIntegerField(unique=True, validators=[django.core.validators.MinLengthValidator(12), django.core.validators.MaxLengthValidator(12)], verbose_name='Aadhar Number')),
                ('pan', models.CharField(max_length=10, unique=True, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.RegexValidator('^[a-zA-z]{5}[0-9]{4}[a-zA-Z]{1}$')], verbose_name='Aadhar Number')),
                ('requests_completed', models.IntegerField(default=0, verbose_name='Requests Completed')),
                ('rating', models.DecimalField(decimal_places=2, default=0, max_digits=3, verbose_name='Rating')),
                ('worker_type', models.CharField(choices=[('electrician', 'electrician'), ('plumber', 'plumber')], max_length=15)),
                ('is_available', models.BooleanField(default=False, verbose_name='Is Available')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Worker',
                'verbose_name_plural': 'Workers',
            },
        ),
    ]
