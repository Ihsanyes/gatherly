from django.shortcuts import render, redirect, HttpResponse
from django.template.context_processors import request

from eventapp.models import CreateEvent,Service
from .models import UserSignup
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User, auth

# Create your views here.

def login(request):
    if request.method == "POST":
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        # Check if the user exists by email or phone number
        user = UserSignup.objects.filter(Q(email=identifier) | Q(phone_number=identifier)).first()

        # Validate the password
        if user and check_password(password, user.password):
            request.session['user_id'] = user.id  # Store user ID in session

            return redirect('/home/')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

def logout(request):
    del request.session['user_id'] # Safely remove the session key
    return redirect('/login/')

def signup(request):
    if request.method == "POST":
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        name = request.POST.get('name')

        # Check for duplicate entries
        if UserSignup.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('/signup/')
        elif UserSignup.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'Phone number already exists')
            return redirect('/signup/')

        # Check if passwords match
        if password != repassword:
            messages.error(request, 'Passwords do not match')
            return redirect('/signup/')

        # Create a new user with hashed password
        obj = UserSignup(
            name=name,
            email=email,
            phone_number=phone_number,
            password=make_password(password)  # Hash the password
        )
        obj.save()

        return redirect('/login/')

    return render(request, 'signup.html')

def login_home(request):
    return render(request, 'home.html')

def home(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        obj = UserSignup.objects.get(id=user_id)
        event_obj = CreateEvent.objects.all()
        services = Service.objects.all()  # Fetch all services for the dropdown
        
        selected_category = request.GET.get('category', '')  # Get selected category from the request

        if selected_category:
            event_obj = CreateEvent.objects.filter(select_services__name=selected_category)
        else:
            event_obj = CreateEvent.objects.all()  # If no category is selected, show all events
            

        return render(request, 'home.html', {'user': obj,'event':event_obj,'services':services})
    else:
        return redirect('/home/'),render(request, 'home.html',{'event':event_obj,'services':services})

def about(request):
    return render(request,'about.html')


