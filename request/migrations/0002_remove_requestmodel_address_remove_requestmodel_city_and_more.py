# Generated by Django 4.1.7 on 2023-03-19 13:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_profile_profile_picture'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestmodel',
            name='address',
        ),
        migrations.RemoveField(
            model_name='requestmodel',
            name='city',
        ),
        migrations.RemoveField(
            model_name='requestmodel',
            name='country',
        ),
        migrations.RemoveField(
            model_name='requestmodel',
            name='email',
        ),
        migrations.RemoveField(
            model_name='requestmodel',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='requestmodel',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='requestmodel',
            name='name',
        ),
        migrations.RemoveField(
            model_name='requestmodel',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='requestmodel',
            name='pincode',
        ),
        migrations.RemoveField(
            model_name='requestmodel',
            name='state',
        ),
        migrations.AddField(
            model_name='requestmodel',
            name='is_closed',
            field=models.BooleanField(default=False, verbose_name='Is Closed'),
        ),
        migrations.AddField(
            model_name='requestmodel',
            name='is_emergency',
            field=models.BooleanField(default=False, verbose_name='Is Emergency'),
        ),
        migrations.AddField(
            model_name='requestmodel',
            name='is_forwarded',
            field=models.BooleanField(default=False, verbose_name='Is Forwarded'),
        ),
        migrations.AddField(
            model_name='requestmodel',
            name='issue',
            field=models.TextField(default='', verbose_name='Issue'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requestmodel',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.location', verbose_name='Location ID'),
        ),
        migrations.AlterField(
            model_name='requestmodel',
            name='request_id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Request ID'),
        ),
        migrations.AlterField(
            model_name='requestmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User ID'),
        ),
        migrations.CreateModel(
            name='FeedbackModel',
            fields=[
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='request.requestmodel', verbose_name='Request ID')),
                ('feedback', models.TextField(verbose_name='Feedback')),
                ('time_of_feedback', models.DateTimeField(verbose_name='Time of Feedback')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User ID')),
            ],
            options={
                'verbose_name': 'Feedback',
                'verbose_name_plural': 'Feedbacks',
            },
        ),
    ]