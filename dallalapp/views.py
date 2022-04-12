from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def home(request):
    return render(request, 'home.html')


def sign_up(request):
    if request.method == 'POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # check inputs
        if password1 != password2 and password1 < 8:
            print("error:enter the password correctly")
            return render(request, 'sign_up.html')

        if len(username) < 2:
            print("error:must be grater than 2 letter")
            return render(request, 'sign_up.html')

        if not username.isalnum:
            print("error:must be number and letters only")
            return render(request, 'sign_up.html')

        # creating user
        #import user
        users = User.objects.create_user(username, email, password1)
        users.first_name = fname
        users.last_name = lname
        users.save()
        return redirect('home')

    return render(request, 'sign_Up.html')


def sign_in(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            print("loggedin")
            return redirect('home')

        else:
            print('cant login try again ')
            return HttpResponse("Fuck off first create a account")

    return render(request, 'sign_in.html')


def log_out(request):

    logout(request)
    print("logedohgcalhv")

    return redirect('home')


def add(request):
    return HttpResponse('hello')
