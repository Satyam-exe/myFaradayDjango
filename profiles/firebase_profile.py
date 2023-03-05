from django.contrib import messages
from firebase_admin import auth, exceptions

from authentication.firebase_config import ref

from authentication.models import CustomFirebaseUser

from .models import Profile


users_ref = ref.child('users')


def update_profile(
        request,
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
        country=None,
        longitude=None,
        latitude=None,
        profile_picture=None,
):
    try:
        if first_name:
            users_ref.child(request.session.get('firebase_uid')).update({
                'first_name': first_name
            })
            CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid')).update(first_name=first_name)
            CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid')).save()
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).update(first_name=first_name)
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).save()
        if last_name:
            users_ref.child(request.session.get('firebase_uid')).update({
                'last_name': last_name
            })
            CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid')).update(last_name=last_name)
            CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid')).save()
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).update(last_name=last_name)
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).save()
        if first_name and last_name:
            auth.update_user(
                uid=request.session.get('firebase_uid'),
                display_name=f'{first_name} {last_name}'
            )
        if email:
            users_ref.child(request.session.get('firebase_uid')).update({
                'email': email
            })
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).update(email=email)
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).save()
        if phone_number:
            users_ref.child(request.session.get('firebase_uid')).update({
                'phone_number': phone_number
            })
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).update(phone_number=phone_number)
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).save()
        if date_of_birth:
            users_ref.child(request.session.get('firebase_uid')).update({
                'date_of_birth': date_of_birth
            })
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).update(date_of_birth=date_of_birth)
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).save()
        if gender:
            users_ref.child(request.session.get('firebase_uid')).update({
                'gender': gender
            })
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).update(gender=gender)
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).save()
        if address1:
            users_ref.child(request.session.get('firebase_uid')).update({
                'address1': address1
            })
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).update(address1=address1)
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).save()
        if address2:
            users_ref.child(request.session.get('firebase_uid')).update({
                'address2': address2
            })
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).update(address2=address2)
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).save()
        if city:
            users_ref.child(request.session.get('firebase_uid')).update({
                'city': city
            })
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).update(city=city)
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).save()
        if pincode:
            users_ref.child(request.session.get('firebase_uid')).update({
                'pincode': pincode
            })
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).update(pincode=pincode)
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).save()
        if state:
            users_ref.child(request.session.get('firebase_uid')).update({
                'state': state
            })
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).update(state=state)
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).save()
        if country:
            users_ref.child(request.session.get('firebase_uid')).update({
                'country': country
            })
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).update(country=country)
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).save()
        if latitude:
            users_ref.child(request.session.get('firebase_uid')).update({
                'latitude': latitude
            })
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).update(latitude=latitude)
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).save()
        if longitude:
            users_ref.child(request.session.get('firebase_uid')).update({
                'longitude': longitude
            })
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).update(longitude=longitude)
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).save()
        if profile_picture:
            users_ref.child(request.session.get('firebase_uid')).update({
                'profile_picture': profile_picture
            })
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).update(profile_picture=profile_picture)
            Profile.objects.get(user=CustomFirebaseUser.objects.get(firebase_uid=request.session.get('firebase_uid'))).save()
    except exceptions.FirebaseError:
        return messages.error(request, 'An error occurred while updating your account. Please try again')
    except Exception as e:
        return messages.error(request, str(e))


def get_profile(firebase_uid):
    return users_ref.child(firebase_uid).get()


def get_first_name_from_firebase_profile(firebase_uid):
    return users_ref.child(firebase_uid).child('first_name').get()


def get_last_name_from_firebase_profile(firebase_uid):
    return users_ref.child(firebase_uid).child('last_name').get()


def get_email_from_firebase_profile(firebase_uid):
    return users_ref.child(firebase_uid).child('email').get()


def get_phone_number_from_firebase_profile(firebase_uid):
    return users_ref.child(firebase_uid).child('phone_number').get()


def get_date_of_birth_from_firebase_profile(firebase_uid):
    return users_ref.child(firebase_uid).child('date_of_birth').get()


def get_gender_from_firebase_profile(firebase_uid):
    return users_ref.child(firebase_uid).child('gender').get()


def get_address1_from_firebase_profile(firebase_uid):
    return users_ref.child(firebase_uid).child('address1').get()


def get_address2_from_firebase_profile(firebase_uid):
    return users_ref.child(firebase_uid).child('address2').get()


def get_city_from_firebase_profile(firebase_uid):
    return users_ref.child(firebase_uid).child('city').get()


def get_pincode_from_firebase_profile(firebase_uid):
    return users_ref.child(firebase_uid).child('pincode').get()


def get_state_from_firebase_profile(firebase_uid):
    return users_ref.child(firebase_uid).child('state').get()


def get_country_from_firebase_profile(firebase_uid):
    return users_ref.child(firebase_uid).child('country').get()


def get_latitude_from_firebase_profile(firebase_uid):
    return users_ref.child(firebase_uid).child('latitude').get()


def get_longitude_from_firebase_profile(firebase_uid):
    return users_ref.child(firebase_uid).child('longitude').get()


def get_profile_picture_from_firebase_profile(firebase_uid):
    return users_ref.child(firebase_uid).child('profile_picture').get()
