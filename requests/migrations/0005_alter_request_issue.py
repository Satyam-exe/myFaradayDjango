# Generated by Django 4.1.7 on 2023-02-20 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0004_alter_request_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='issue',
            field=models.TextField(max_length=500),
        ),
    ]
