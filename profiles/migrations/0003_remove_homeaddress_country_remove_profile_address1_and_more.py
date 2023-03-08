# Generated by Django 4.1.7 on 2023-03-08 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profileupdates_homeaddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homeaddress',
            name='country',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='address1',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='address2',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='city',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='country',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='pincode',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='state',
        ),
        migrations.AlterField(
            model_name='homeaddress',
            name='state',
            field=models.CharField(choices=[('AN', 'Andaman and Nicobar Islands'), ('AP', 'Andhra Pradesh'), ('AR', 'Arunachal Pradesh'), ('AS', 'Assam'), ('BR', 'Bihar'), ('CG', 'Chhattisgarh'), ('CH', 'Chandigarh'), ('DN', 'Dadra and Nagar Haveli'), ('DD', 'Daman and Diu'), ('DL', 'Delhi'), ('GA', 'Goa'), ('GJ', 'Gujarat'), ('HR', 'Haryana'), ('HP', 'Himachal Pradesh'), ('JK', 'Jammu and Kashmir'), ('JH', 'Jharkhand'), ('KA', 'Karnataka'), ('KL', 'Kerala'), ('LA', 'Ladakh'), ('LD', 'Lakshadweep'), ('MP', 'Madhya Pradesh'), ('MH', 'Maharashtra'), ('MN', 'Manipur'), ('ML', 'Meghalaya'), ('MZ', 'Mizoram'), ('NL', 'Nagaland'), ('OD', 'Odisha'), ('PB', 'Punjab'), ('PY', 'Pondicherry'), ('RJ', 'Rajasthan'), ('SK', 'Sikkim'), ('TN', 'Tamil Nadu'), ('TS', 'Telangana'), ('TR', 'Tripura'), ('UP', 'Uttar Pradesh'), ('UK', 'Uttarakhand'), ('WB', 'West Bengal')], max_length=2, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='profileupdates',
            name='update_type',
            field=models.CharField(choices=[('first_name', 'first_name'), ('last_name', 'last_name'), ('email', 'email'), ('phone_number', 'phone_number'), ('date_of_birth', 'date_of_birth'), ('gender', 'gender'), ('address1', 'address1'), ('address2', 'address2'), ('city', 'city'), ('pincode', 'pincode'), ('state', 'state'), ('latitude', 'latitude'), ('longitude', 'longitude'), ('profile_picture', 'profile_picture')], max_length=50, verbose_name='Update Type'),
        ),
    ]