# Generated by Django 4.1.7 on 2023-02-27 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_customfirebaseuser_last_activity_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customfirebaseuser',
            options={'verbose_name': 'Custom Firebase User', 'verbose_name_plural': 'Custom Firebase Users'},
        ),
    ]