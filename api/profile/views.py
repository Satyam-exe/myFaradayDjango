from django.db import IntegrityError, DatabaseError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.profile import serializers
from api.profile.serializers import ProfileSerializer
from profiles.models import Profile


class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProfileRetrieveAPIView(APIView):
    def get(self, request, pk):
        try:
            serializer = ProfileSerializer(Profile.objects.get(pk=pk))
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response(
                {
                    'error': {
                        'message': 'USER_NOT_FOUND'
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )
        except IntegrityError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT
            )
        except DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'pk': profile.pk,
                        'email': profile.email,
                        'phone_number': profile.phone_number
                    }, status=status.HTTP_200_OK
                )
        except Profile.DoesNotExist:
            return Response(
                {
                    'error': {
                        'message': 'USER_NOT_FOUND'
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )
        except IntegrityError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT
            )
        except DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'pk': profile.pk,
                        'email': profile.email,
                        'phone_number': profile.phone_number
                    }, status=status.HTTP_200_OK
                )
        except Profile.DoesNotExist:
            return Response(
                {
                    'error': {
                        'message': 'USER_NOT_FOUND'
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )
        except IntegrityError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                    }
                }, status=status.HTTP_409_CONFLICT
            )
        except DatabaseError as e:
            return Response(
                {
                    'error': {
                        'message': str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

