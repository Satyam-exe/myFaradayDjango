import datetime
import random
from io import BytesIO

import pytz
import requests
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile

from authentication.models import CustomUser

from .models import Profile, ProfileUpdates, Location


def update_profile(
        uid,
        first_name=None,
        last_name=None,
        email=None,
        phone_number=None,
        date_of_birth=None,
        gender=None,
        new_address=None,
        city=None,
        pincode=None,
        state=None,
        longitude=None,
        latitude=None,
        profile_picture=None,
):
    try:
        updates = 0
        if first_name:
            profile = Profile.objects.get(pk=uid)
            old_value = profile.first_name
            profile.first_name = first_name
            profile.save()
            new_update = ProfileUpdates(
                user=profile,
                update_type='first_name',
                updated_from=old_value,
                updated_to=first_name,
                updated_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            )
            new_update.save()
            updates += 1
        if last_name:
            profile = Profile.objects.get(pk=uid)
            old_value = profile.last_name
            profile.last_name = last_name
            profile.save()
            new_update = ProfileUpdates(
                user=profile,
                update_type='last_name',
                updated_from=old_value,
                updated_to=last_name,
                updated_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            )
            new_update.save()
            updates += 1
        if email:
            profile = Profile.objects.get(pk=uid)
            old_value = profile.email
            profile.email = email
            profile.save()
            new_update = ProfileUpdates(
                user=profile,
                update_type='email',
                updated_from=old_value,
                updated_to=email,
                updated_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            )
            new_update.save()
            updates += 1
        if phone_number:
            profile = Profile.objects.get(pk=uid)
            old_value = profile.phone_number
            profile.phone_number = phone_number
            profile.save()
            new_update = ProfileUpdates(
                user=profile,
                update_type='phone_number',
                updated_from=old_value,
                updated_to=phone_number,
                updated_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            )
            new_update.save()
            updates += 1
        if date_of_birth:
            profile = Profile.objects.get(pk=uid)
            old_value = profile.date_of_birth
            profile.date_of_birth = date_of_birth
            profile.save()
            new_update = ProfileUpdates(
                user=profile,
                update_type='date_of_birth',
                updated_from=old_value,
                updated_to=date_of_birth,
                updated_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            )
            new_update.save()
            updates += 1
        if gender:
            profile = Profile.objects.get(pk=uid)
            old_value = profile.gender
            profile.gender = gender
            profile.save()
            new_update = ProfileUpdates(
                user=profile,
                update_type='gender',
                updated_from=old_value,
                updated_to=gender,
                updated_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            )
            new_update.save()
            updates += 1
        if new_address:
            address = Location.objects.get(pk=uid)
            old_value = address.address1
            address.address = new_address
            address.save()
            new_update = ProfileUpdates(
                user=address.user,
                update_type='address',
                updated_from=old_value,
                updated_to=new_address,
                updated_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            )
            new_update.save()
            updates += 1
        if city:
            address = Location.objects.get(pk=uid)
            old_value = address.city
            address.city = city
            address.save()
            new_update = ProfileUpdates(
                user=address.user,
                update_type='city',
                updated_from=old_value,
                updated_to=city,
                updated_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            )
            new_update.save()
            updates += 1
        if pincode:
            address = Location.objects.get(pk=uid)
            old_value = address.pincode
            address.pincode = pincode
            address.save()
            new_update = ProfileUpdates(
                user=address.user,
                update_type='pincode',
                updated_from=old_value,
                updated_to=pincode,
                updated_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            )
            new_update.save()
            updates += 1
        if state:
            address = Location.objects.get(pk=uid)
            old_value = address.state
            address.state = state
            address.save()
            new_update = ProfileUpdates(
                user=address.user,
                update_type='state',
                updated_from=old_value,
                updated_to=state,
                updated_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            )
            new_update.save()
            updates += 1
        if latitude:
            address = Location.objects.get(pk=uid)
            old_value = address.latitude
            address.latitude = latitude
            address.save()
            new_update = ProfileUpdates(
                user=address.user,
                update_type='latitude',
                updated_from=old_value,
                updated_to=latitude,
                updated_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            )
            new_update.save()
            updates += 1
        if longitude:
            address = Location.objects.get(pk=uid)
            old_value = address.longitude
            address.longitude = longitude
            address.save()
            new_update = ProfileUpdates(
                user=address.user,
                update_type='longitude',
                updated_from=old_value,
                updated_to=longitude,
                updated_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            )
            new_update.save()
            updates += 1
        if profile_picture:
            profile = Profile.objects.get(pk=uid)
            old_value = profile.profile_picture
            profile.profile_picture = profile_picture
            profile.save()
            new_update = ProfileUpdates(
                user=profile,
                update_type='profile_picture',
                updated_from=old_value,
                updated_to=profile_picture,
                updated_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            )
            new_update.save()
            updates += 1
        if updates > 0:
            return True
        else:
            return False
    except CustomUser.DoesNotExist:
        return False
    except Profile.DoesNotExist:
        return False


def generate_default_profile_picture_content_file(user: CustomUser):
    image_url = f"https://ui-avatars.com/api/?background=random&name={user.first_name}+{user.last_name}/"

    response = requests.get(image_url, stream=True)
    response.raise_for_status()

    image = Image.open(BytesIO(response.content)).convert('RGB')

    # Convert the image to a JPEG format and save it to a memory buffer
    image_buffer = BytesIO()
    image.save(image_buffer, format='JPEG')
    image_buffer.seek(0)

    return ContentFile(image_buffer.read())
