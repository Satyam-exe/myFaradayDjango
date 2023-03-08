import django.db
import rest_framework.generics
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from authentication.functions import verify_code, send_confirm_password_reset_link, send_email_verification_link
from authentication.models import CustomUser
from .serializers import SignUpSerializer, LogInSerializer, CustomUserSerializer, \
    ConfirmPasswordResetSerializer, ResetPasswordSerializer, EmailVerificationSerializer


class SignUpAPIView(APIView):

    def post(self, request):
        try:
            serializer = SignUpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            email_conflict = CustomUser.objects.filter(email=serializer.validated_data.get('email')).exists()
            phone_conflict = CustomUser.objects.filter(phone_number=serializer.validated_data.get('phone_number')).exists()

            if email_conflict and phone_conflict:
                message = 'BOTH_IDENTIFIERS_ALREADY_IN_USE'
            elif email_conflict:
                message = 'EMAIL_ALREADY_IN_USE'
            elif phone_conflict:
                message = 'PHONE_NUMBER_ALREADY_IN_USE'
            else:
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
                        'is_email_verified': new_user.is_email_verified
                    }, status=status.HTTP_201_CREATED
                )

            return Response(
                {
                    'error': {
                        'message': message,
                    }
                }, status=status.HTTP_409_CONFLICT
            )

        except (django.db.IntegrityError, ValidationError) as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT if isinstance(e, django.db.IntegrityError) else status.HTTP_400_BAD_REQUEST
            )

        except django.db.DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogInAPIView(APIView):

    def post(self, request):
        serializer = LogInSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            try:
                user = authenticate(request=request, email=email, password=password)
                if user:
                    if user.is_email_verified:
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


class UserListAPIView(rest_framework.generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserRetrieveAPIView(APIView):

    def get(self, request, pk):
        serializer = CustomUserSerializer(CustomUser.objects.get(pk=pk))
        return Response(serializer.data)

    def put(self, request, pk, **kwargs):
        serializer = CustomUserSerializer(CustomUser.objects.get(pk=pk).update(**kwargs))
        return Response(serializer.data)

    def patch(self, request, pk, **kwargs):
        serializer = CustomUserSerializer(CustomUser.objects.get(pk=pk).update(**kwargs))
        return Response(serializer.data)

    def delete(self, request, pk):
        CustomUser.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRetrieveWithEmailAPIView(APIView):

    def get(self, request, email):
        serializer = CustomUserSerializer(CustomUser.objects.get(email=email))
        return Response(serializer.data)

    def put(self, request, email, **kwargs):
        serializer = CustomUserSerializer(CustomUser.objects.get(email=email).update(**kwargs))
        return Response(serializer.data)

    def patch(self, request, email, **kwargs):
        serializer = CustomUserSerializer(CustomUser.objects.get(email=email).update(**kwargs))
        return Response(serializer.data)

    def delete(self, request, email):
        CustomUser.objects.get(email=email).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRetrieveWithPhoneNumberAPIView(APIView):

    def get(self, request, phone_number):
        serializer = CustomUserSerializer(CustomUser.objects.get(phone_number=phone_number))
        return Response(serializer.data)

    def put(self, request, phone_number, **kwargs):
        serializer = CustomUserSerializer(CustomUser.objects.get(phone_number=phone_number).update(**kwargs))
        return Response(serializer.data)

    def patch(self, request, phone_number, **kwargs):
        serializer = CustomUserSerializer(CustomUser.objects.get(phone_number=phone_number).update(**kwargs))
        return Response(serializer.data)

    def delete(self, request, phone_number):
        CustomUser.objects.get(phone_number=phone_number).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
