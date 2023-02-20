from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserProfileForm
from accounts.models import CustomUser
from .models import CustomUserProfile


@login_required
def profile_form_view(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user_id = user.id
            profile.email = user.email
            profile.phone_number = user.phone_number
            profile.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('/requests/create/')
    else:
        try:
            profile = CustomUserProfile.objects.get(user=user)
            form = CustomUserProfileForm(instance=profile)
        except CustomUserProfile.DoesNotExist:
            form = CustomUserProfileForm()

    return render(request, 'editprofile.html', {'form': form})