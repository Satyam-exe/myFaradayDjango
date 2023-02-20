from django.db import models
from accounts.models import CustomUser


class CustomUserProfile(models.Model):
    GENDER_CHOICES = [
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Others'),
    ]
    INDIAN_STATE_CHOICES = [
        ("AN", "Andaman and Nicobar Islands"),
        ("AP", "Andhra Pradesh"),
        ("AR", "Arunachal Pradesh"),
        ("AS", "Assam"),
        ("BR", "Bihar"),
        ("CG", "Chhattisgarh"),
        ("CH", "Chandigarh"),
        ("DN", "Dadra and Nagar Haveli"),
        ("DD", "Daman and Diu"),
        ("DL", "Delhi"),
        ("GA", "Goa"),
        ("GJ", "Gujarat"),
        ("HR", "Haryana"),
        ("HP", "Himachal Pradesh"),
        ("JK", "Jammu and Kashmir"),
        ("JH", "Jharkhand"),
        ("KA", "Karnataka"),
        ("KL", "Kerala"),
        ("LA", "Ladakh"),
        ("LD", "Lakshadweep"),
        ("MP", "Madhya Pradesh"),
        ("MH", "Maharashtra"),
        ("MN", "Manipur"),
        ("ML", "Meghalaya"),
        ("MZ", "Mizoram"),
        ("NL", "Nagaland"),
        ("OD", "Odisha"),
        ("PB", "Punjab"),
        ("PY", "Pondicherry"),
        ("RJ", "Rajasthan"),
        ("SK", "Sikkim"),
        ("TN", "Tamil Nadu"),
        ("TS", "Telangana"),
        ("TR", "Tripura"),
        ("UP", "Uttar Pradesh"),
        ("UK", "Uttarakhand"),
        ("WB", "West Bengal"),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=45, verbose_name='First Name')
    last_name = models.CharField(max_length=45, verbose_name='Last Name')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Gender')
    date_of_birth = models.DateField(verbose_name='Date of Birth')
    address = models.CharField(max_length=500, verbose_name='Address')
    email = models.EmailField(blank=True, null=True, verbose_name='Email Address')
    phone_number = models.CharField(max_length=10, verbose_name='Mobile Number')
    secondary_phone_number = models.CharField(max_length=10, blank=True, null=True, verbose_name='Alternate Mobile Number')
    state = models.CharField(max_length=2, choices=INDIAN_STATE_CHOICES, verbose_name='State')
    city = models.CharField(max_length=50, verbose_name='City')
    pincode = models.CharField(max_length=6, verbose_name='Pincode')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Latitude')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Longitutde')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'User Profile',
        verbose_name_plural = 'User Profiles'
