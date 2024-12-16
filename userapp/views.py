from django.shortcuts import render,redirect,HttpResponse
from .models import UserSignup
from django.contrib import messages
from django.contrib.auth.models import User,auth
# Create your views here.
# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('/home/')
#         else:
#             messages.error(request, 'Invalid username or password')
#     return render(request,'login.html')
#
# def logout(request):
#     auth.logout(request)
#     return redirect('')


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = UserSignup.objects.filter(username=username, password=password).first()
        if user:
            # Store username in the session
            request.session['username'] = username
            return redirect('/home/')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


def logout(request):
    del request.session['username']
    return redirect('/home/')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
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
        elif UserSignup.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('/signup/')

        # Check if passwords match

        if password != repassword:
            messages.error(request, 'Passwords do not match')
            return redirect('/signup/')  # Use named URL for better maintainability


        # Create a new user
        obj = UserSignup(
            name=name,
            email=email,
            phone_number=phone_number,
            username=username,
            password=password
        )
        obj.save()

        # messages.success(request, 'Signup successful! Please log in.')
        return redirect('/login/')  # Use named URL

    return render(request, 'signup.html')  # Handle GET requests


def login_home(request):
    return render(request,'login_home.html')

def home(request):
    if 'username' in request.session:
        return render(request,'home.html')
    else:
        return redirect('/')

def event_card(request):
    if 'usename' in request.session:
        return render(request,'eventcard.html')
    else:
        return redirect('/signup/')
def card_list(request):
    if 'username' in request.session:
        return render(request,'card_list.html')
    else:
        return redirect('/signup/')