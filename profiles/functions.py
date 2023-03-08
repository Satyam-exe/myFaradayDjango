import datetime

import pytz

from authentication.models import CustomUser

from .models import Profile, ProfileUpdates, HomeAddress


def update_profile(
        uid,
        first_name=None,
        last_name=None,
        email=None,
        phone_number=None,
        date_of_birth=None,
        gender=None,
        address1=None,
        address2=None,
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
        if address1:
            address = HomeAddress.objects.get(pk=uid)
            old_value = address.address1
            address.address1 = address1
            address.save()
            new_update = ProfileUpdates(
                user=address.user,
                update_type='address1',
                updated_from=old_value,
                updated_to=address1,
                updated_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            )
            new_update.save()
            updates += 1
        if address2:
            address = HomeAddress.objects.get(pk=uid)
            old_value = address.address2
            address.address2 = address2
            address.save()
            new_update = ProfileUpdates(
                user=address.user,
                update_type='address2',
                updated_from=old_value,
                updated_to=address2,
                updated_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            )
            new_update.save()
            updates += 1
        if city:
            address = HomeAddress.objects.get(pk=uid)
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
            address = HomeAddress.objects.get(pk=uid)
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
            address = HomeAddress.objects.get(pk=uid)
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
            address = HomeAddress.objects.get(pk=uid)
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
            address = HomeAddress.objects.get(pk=uid)
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
