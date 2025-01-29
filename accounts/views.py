from django.shortcuts import render
from .forms import RegistrationForm
from .models import Account
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            # Check if email already exists
            if Account.objects.filter(email=email).exists():
                return JsonResponse({'message': 'Email already exists. Please use a different email.'}, status=400)

            # Create the user
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )
            user.phone_number = phone_number
            user.save()
            return JsonResponse({
                'message': 'Your account has been created successfully!',
                'redirect_url': reverse('login') 
                }, status=200)
            
        else:
            # Include non-field errors in the response
            errors = {
                field: [error for error in error_list]
                for field, error_list in form.errors.items()
            }
            return JsonResponse({
                'message': 'There were errors in your form.',
                'errors': errors
            }, status=400)
    else:
        form = RegistrationForm()
        context = {'form': form}
        return render(request, 'mainshop/accounts/register.html', context)

 
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return JsonResponse({'status': 'success', 'message': 'You are now logged in.',
                                 'redirect_url': reverse('home') 
                                 }, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid login credentials.'}, status=401)

    return render(request, 'mainshop/accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')  # Redirect to a public page instead of rendering login.html



