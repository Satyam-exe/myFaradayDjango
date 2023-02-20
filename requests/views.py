from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RequestForm
from .models import Request


@login_required
def request_form_view(request):
    user = request.user
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            requestform = form.save(commit=False)
            requestform.user = user
            requestform.name = f"{user.customuserprofile.first_name} {user.customuserprofile.last_name}"
            requestform.email = user.customuserprofile.email
            requestform.phone_number = user.customuserprofile.phone_number
            requestform.address = user.customuserprofile.address
            requestform.pincode = user.customuserprofile.pincode
            requestform.save()
            messages.success(request, 'Request sent successfully')
            return redirect('/')
    else:
        form = RequestForm()

    return render(request, 'requestform.html', {'form': form})