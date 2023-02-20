from django.shortcuts import render


# Create your views here.
def hello_world_view(request):
    return render(request, 'home.html', {})
