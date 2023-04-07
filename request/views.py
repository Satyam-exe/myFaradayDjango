import requests
from django.contrib import messages
from django.shortcuts import render, redirect

from api.request import serializers
from authentication.models import CustomUser
from profiles.models import Location
from request import forms


def request_create_view(request):
    if request.method == 'POST':
        form = forms.RequestForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['user'] = CustomUser.objects.get(id=request.user.id)
            form_data['location'] = Location.objects.get(user_id=request.user.id)
            serializer = serializers.RequestSerializer(data=form_data)
            if serializer.is_valid():
                data = serializer.validated_data
                url = 'http://localhost:8000/api/request/'
                response = requests.post(url=url, data=data)
                if response.status_code == 201:
                    return redirect('home')
                elif response.status_code == 500:
                    messages.error(request, 'Internal Server Error. Please Try Again.')
                elif response.status_code == 409:
                    messages.error(request, 'Conflicting Request. Please Try Again.')
                else:
                    messages.error(request, 'Something Went Wrong. Please Try Again')
    else:
        form = forms.RequestForm
    return render(request, 'signup.html', {'form': form})
