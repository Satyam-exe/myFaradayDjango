import django.db
import rest_framework.generics
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from authentication.functions import verify_code
from authentication.models import CustomUser
from .serializers import SignUpSerializer, LogInSerializer, CustomUserSerializer, URLCodeSerializer


class SignUpAPIView(APIView):

    @transaction.atomic
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            try:
                new_user = serializer.create(validated_data=serializer.validated_data)
                return Response(
                    {
                        'uid': new_user.pk,
                        'email': new_user.email,
                        'phone_number': new_user.phone_number
                    }, status=status.HTTP_201_CREATED
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


class LogInAPIView(APIView):

    def post(self, request):
        serializer = LogInSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            try:
                user = authenticate(request=request, email=email, password=password)
                if user:
                    return Response(
                        {
                            'user': CustomUserSerializer(user).data
                        }, status=status.HTTP_200_OK
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
        serializer = URLCodeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                code = serializer.validated_data.get('code')
                list_returned = verify_code(code, 'email_verification') or None
                if list_returned:
                    user = list_returned[0]
                    code_object = list_returned[1]
                    if user and code_object:
                        user.update(is_email_verified=True)
                        code_object.update(is_user=True)
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


class UserListView(rest_framework.generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserRetrieveView(APIView):

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
