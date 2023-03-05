# Generated by Django 4.1.7 on 2023-03-05 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_profile_firebase_uid'),
        ('request', '0002_alter_requestmodel_firebase_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestmodel',
            name='firebase_uid',
            field=models.ForeignKey(db_column='firebase_uid', on_delete=django.db.models.deletion.PROTECT, to='profiles.profile', verbose_name='Firebase User ID'),
        ),
    ]