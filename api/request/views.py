import django.db

from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from api.request import serializers
from request.models import Request


class RequestAPIView(ListCreateAPIView):
    queryset = Request.objects.all()
    serializer_class = serializers.RequestSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            serializer = serializers.RequestSerializer(data=request.data)
            if serializer.is_valid():
                new_request: Request = serializer.create(validated_data=serializer.validated_data)
                return Response(
                    {
                        'request_id': new_request.id,
                        'user_id': new_request.user_id,
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