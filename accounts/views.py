from django.shortcuts import render

# Create your views here.

def register(request):
    return render(request, 'mainshop/accounts/register.html')

def login(request):
    return render(request, 'mainshop/accounts/login.html')

def logout(request):
    pass

