import datetime
import django.db
import pytz

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.functions import verify_code, send_confirm_password_reset_link, send_email_verification_link, \
    generate_mobile_auth_token, verify_mobile_auth_token
from authentication.models import CustomUser, MobileAuthToken
from api.authentication.serializers import SignUpSerializer, LogInSerializer, CustomUserSerializer, \
    ConfirmPasswordResetSerializer, ResetPasswordSerializer, EmailVerificationSerializer, \
    VerifyMobileAuthTokenSerializer, RevokeMobileAuthTokenSerializer


class LogInAPIView(APIView):

    def post(self, request):
        serializer = LogInSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            request_platform = serializer.validated_data.get('request_platform') or None
            requested_time_in_days = serializer.validated_data.get('requested_time_in_days') or None
            try:
                user = authenticate(request=request, email=email, password=password)
                if user:
                    if user.is_email_verified:
                        if request_platform == 'flutter' and requested_time_in_days:
                            token = generate_mobile_auth_token(
                                uid=user.pk,
                                requested_time_in_days=requested_time_in_days
                            )
                            user.last_login = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
                            return Response(
                                {
                                    'uid': user.pk,
                                    'token': token
                                }, status=status.HTTP_200_OK
                            )
                        return Response(
                            {
                                'uid': user.pk
                            }, status=status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            {
                                'error': {
                                    'message': 'EMAIL_NOT_VERIFIED'
                                }
                            }, status=status.HTTP_401_UNAUTHORIZED
                        )
                else:
                    return Response(
                        {
                            'error': {
                                'message': 'INVALID_CREDENTIALS'
                            }
                        }, status=status.HTTP_404_NOT_FOUND
                    )
            except django.db.IntegrityError as e:
                return Response(
                    {
                        'error': {
                            'message': str(e),
                        }
                    }, status=status.HTTP_409_CONFLICT
                )
            except django.db.DatabaseError as e:
                return Response(
                    {
                        'error': {
                            'message': str(e)
                        }
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except ValidationError as e:
                return Response(
                    {
                        'error': {
                            'message': str(e)
                        }
                    }, status=status.HTTP_400_BAD_REQUEST
                )


class EmailVerificationAPIView(APIView):

    def post(self, request):
        print('method is  post')
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data.get('code'))
            print('serializer is valid')
            print(serializer.validated_data)
            try:
                code = serializer.validated_data.get('code')
                list_returned = verify_code(code, 'email_verification')
                print(list_returned)
                if list_returned:
                    print('list is returned' + str(list_returned))
                    user = list_returned[0]
                    code_object = list_returned[1]
                    if user and code_object:
                        user.is_email_verified = True
                        user.save()
                        code_object.is_used = True
                        code_object.save()
                        return Response(
                            {
                                'uid': user.pk,
                                'email': user.email,
                                'phone_number': user.phone_number
                            }, status=status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            {
                                'error': {
                                    'message': 'INVALID_CODE'
                                }
                            }, status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {
                            'error': {
                                'message': 'INVALID_CODE'
                            }
                        }, status=status.HTTP_400_BAD_REQUEST
                    )
            except django.db.IntegrityError as e:
                return Response(
                    {
                        'error': {
                            'message': str(e),
                        }
                    }, status=status.HTTP_409_CONFLICT
                )
            except django.db.DatabaseError as e:
                return Response(
                    {
                        'error': {
                            'message': str(e)
                        }
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


class PasswordResetAPIView(APIView):

    def post(self, request):
        print('method is  post')
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            print('serializer is valid')
            print(serializer.validated_data)
            try:
                email = serializer.validated_data.get('email')
                if send_confirm_password_reset_link(email):
                    return Response(
                        {
                            'email': email
                        }, status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'error': {
                                'message': 'USER_NOT_FOUND'
                            }
                        }, status=status.HTTP_404_NOT_FOUND
                    )
            except django.db.IntegrityError as e:
                return Response(
                    {
                        'error': {
                            'message': str(e),
                        }
                    }, status=status.HTTP_409_CONFLICT
                )
            except django.db.DatabaseError as e:
                return Response(
                    {
                        'error': {
                            'message': str(e)
                        }
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


class ConfirmPasswordResetAPIView(APIView):

    def post(self, request):
        print('method is  post')
        serializer = ConfirmPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            print('serializer is valid')
            print(serializer.validated_data)
            try:
                code = serializer.validated_data.get('code')
                password = serializer.validated_data.get('password')
                list_returned = verify_code(code, 'password_reset_confirm') or None
                if list_returned:
                    print('list is returned' + str(list_returned))
                    user = list_returned[0]
                    code_object = list_returned[1]
                    if user and code_object:
                        user.set_password(password)
                        user.save()
                        code_object.is_used = True
                        code_object.save()
                        if MobileAuthToken.objects.filter(user=user).exists():
                            MobileAuthToken.objects.filter(user=user).is_revoked = True
                        return Response(
                            {
                                'uid': user.pk,
                                'email': user.email,
                                'phone_number': user.phone_number
                            }, status=status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            {
                                'error': {
                                    'message': 'INVALID_CODE'
                                }
                            }, status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {
                            'error': {
                                'message': 'INVALID_CODE'
                            }
                        }, status=status.HTTP_400_BAD_REQUEST
                    )
            except django.db.IntegrityError as e:
                return Response(
                    {
                        'error': {
                            'message': str(e),
                        }
                    }, status=status.HTTP_409_CONFLICT
                )
            except django.db.DatabaseError as e:
                return Response(
                    {
                        'error': {
                            'message': str(e)
                        }
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


class UserAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            serializer = SignUpSerializer(data=request.data)
            if serializer.is_valid():
                email_conflict = CustomUser.objects.filter(email=serializer.validated_data.get('email')).exists()
                phone_conflict = CustomUser.objects.filter(
                    phone_number=serializer.validated_data.get('phone_number')).exists()
                if email_conflict and phone_conflict:
                    message = 'BOTH_IDENTIFIERS_ALREADY_IN_USE'
                elif email_conflict:
                    message = 'EMAIL_ALREADY_IN_USE'
                elif phone_conflict:
                    message = 'PHONE_NUMBER_ALREADY_IN_USE'
                else:
                    message = None
                if message is not None:
                    return Response(
                        {
                            'error': {
                                'message': message,
                            }
                        }, status=status.HTTP_409_CONFLICT
                    )
                validate_password(password=serializer.validated_data.get('password'))
                new_user = serializer.create(validated_data=serializer.validated_data)
                return Response(
                    {
                        'uid': new_user.pk,
                        'email': new_user.email,
                        'phone_number': new_user.phone_number,
                        'first_name': new_user.first_name,
                        'last_name': new_user.last_name,
                        'is_superuser': new_user.is_superuser,
                        'is_staff': new_user.is_staff,
                        'is_email_verified': new_user.is_email_verified,
                    }, status=status.HTTP_201_CREATED
                )
        except ValidationError:
            return Response(
                {
                    'error': {
                        'message': 'WEAK_PASSWORD',
                    }
                }, status=status.HTTP_406_NOT_ACCEPTABLE
            )
        except django.db.IntegrityError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT
            )
        except ValidationError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except django.db.DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserRetrieveAPIView(APIView):

    def get(self, request, pk):
        try:
            serializer = CustomUserSerializer(CustomUser.objects.get(pk=pk))
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response(
                {
                    'error': {
                        'message': 'USER_NOT_FOUND'
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )
        except django.db.IntegrityError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT
            )
        except django.db.DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk, **kwargs):
        try:
            serializer = CustomUserSerializer(CustomUser.objects.get(pk=pk).update(**kwargs))
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response(
                {
                    'error': {
                        'message': 'USER_NOT_FOUND'
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )
        except django.db.IntegrityError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT
            )
        except django.db.DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk, **kwargs):
        try:
            serializer = CustomUserSerializer(CustomUser.objects.get(pk=pk).update(**kwargs))
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response(
                {
                    'error': {
                        'message': 'USER_NOT_FOUND'
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )
        except django.db.IntegrityError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT
            )
        except django.db.DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            CustomUser.objects.get(pk=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response(
                {
                    'error': {
                        'message': 'USER_NOT_FOUND'
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )
        except django.db.IntegrityError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT
            )
        except django.db.DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserRetrieveWithEmailAPIView(APIView):

    def get(self, request, email):
        try:
            serializer = CustomUserSerializer(CustomUser.objects.get(email=email))
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response(
                {
                    'error': {
                        'message': 'USER_NOT_FOUND'
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )
        except django.db.IntegrityError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT
            )
        except django.db.DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, email, **kwargs):
        try:
            serializer = CustomUserSerializer(CustomUser.objects.get(email=email).update(**kwargs))
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response(
                {
                    'error': {
                        'message': 'USER_NOT_FOUND'
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )
        except django.db.IntegrityError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT
            )
        except django.db.DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, email, **kwargs):
        try:
            serializer = CustomUserSerializer(CustomUser.objects.get(email=email).update(**kwargs))
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response(
                {
                    'error': {
                        'message': 'USER_NOT_FOUND'
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )
        except django.db.IntegrityError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT
            )
        except django.db.DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, email):
        try:
            CustomUser.objects.get(email=email).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response(
                {
                    'error': {
                        'message': 'USER_NOT_FOUND'
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )
        except django.db.IntegrityError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT
            )
        except django.db.DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserRetrieveWithPhoneNumberAPIView(APIView):

    def get(self, request, phone_number):
        try:
            serializer = CustomUserSerializer(CustomUser.objects.get(phone_number=phone_number))
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response(
                {
                    'error': {
                        'message': 'USER_NOT_FOUND'
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )
        except django.db.IntegrityError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT
            )
        except django.db.DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, phone_number, **kwargs):
        try:
            serializer = CustomUserSerializer(CustomUser.objects.get(phone_number=phone_number).update(**kwargs))
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response(
                {
                    'error': {
                        'message': 'USER_NOT_FOUND'
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )
        except django.db.IntegrityError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT
            )
        except django.db.DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, phone_number, **kwargs):
        try:
            serializer = CustomUserSerializer(CustomUser.objects.get(phone_number=phone_number).update(**kwargs))
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response(
                {
                    'error': {
                        'message': 'USER_NOT_FOUND'
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )
        except django.db.IntegrityError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT
            )
        except django.db.DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, phone_number):
        try:
            CustomUser.objects.get(phone_number=phone_number).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response(
                {
                    'error': {
                        'message': 'USER_NOT_FOUND'
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )
        except django.db.IntegrityError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT
            )
        except django.db.DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SendEmailVerificationAPIView(APIView):

    def post(self, request):
        try:
            uid = request.data.get('uid')
            user = CustomUser.objects.get(pk=uid)
            send_email_verification_link(uid=uid)
            return Response(
                {
                    'uid': user.pk,
                    'email': user.email,
                    'phone_number': user.phone_number
                }, status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            return Response(
                {
                    'error': {
                        'message': 'USER_NOT_FOUND',
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )
        except django.db.IntegrityError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT
            )
        except django.db.DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyMobileAuthTokenAPIView(APIView):
    def post(self, request):
        serializer = VerifyMobileAuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = serializer.validated_data.get('token')
                uid = serializer.validated_data.get('uid')
                list_returned = verify_mobile_auth_token(token=token, uid=uid)
                if list_returned:
                    user = list_returned[0]
                    token_object = list_returned[1]
                    if user and token_object:
                        token_object.last_used = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
                        token_object.save()
                        return Response(
                            {
                                'uid': user.pk,
                                'email': user.email,
                                'phone_number': user.phone_number
                            }, status=status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            {
                                'error': {
                                    'message': 'INVALID_TOKEN'
                                }
                            }, status=status.HTTP_403_FORBIDDEN
                        )
                else:
                    return Response(
                        {
                            'error': {
                                'message': 'INVALID_TOKEN'
                            }
                        }, status=status.HTTP_403_FORBIDDEN
                    )
            except django.db.IntegrityError as e:
                return Response(
                    {
                        'error': {
                            'message': str(e),
                        }
                    }, status=status.HTTP_409_CONFLICT
                )
            except django.db.DatabaseError as e:
                return Response(
                    {
                        'error': {
                            'message': str(e)
                        }
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {
                    'error': {
                        'message': 'INVALID_REQUEST'
                    }
                }, status=status.HTTP_400_BAD_REQUEST
            )


class MobileAuthTokenAPIView(APIView):
    def patch(self, request):
        serializer = RevokeMobileAuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token_object = MobileAuthToken.objects.get(pk=serializer.validated_data.get('token'))
                token_object.is_revoked = True
                token_object.save()
                return Response(
                    {
                        'token': token_object.pk,
                        'is_revoked': token_object.is_revoked
                    }, status=status.HTTP_200_OK
                )
            except MobileAuthToken.DoesNotExist:
                return Response(
                    {
                        'error': {
                            'message': 'INVALID_TOKEN'
                        }
                    }, status=status.HTTP_404_NOT_FOUND)
            except django.db.IntegrityError as e:
                return Response(
                    {
                        'error': {
                            'message': str(e),
                        }
                    }, status=status.HTTP_409_CONFLICT
                )
            except django.db.DatabaseError as e:
                return Response(
                    {
                        'error': {
                            'message': str(e)
                        }
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {
                    'error': {
                        'message': 'INVALID_REQUEST'
                    }
                }, status=status.HTTP_400_BAD_REQUEST
            )
