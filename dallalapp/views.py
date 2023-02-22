from datetime import datetime, timedelta
import pytz
import folium

from django.contrib.auth.decorators import login_required

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.core.files.storage import FileSystemStorage

from .models import Dhani, UserComments

from .form import PostForm
# Create your views here.


def home(request):
    if request.method == 'POST':
        searched_query = (request.POST['searched']).capitalize()
        # print(searched_query)
        searched = Dhani.objects.filter(address=searched_query)
        # print(searched)
        context = {
            'posts': searched
        }
        return render(request, 'home.html', context)
    posts = Dhani.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'home.html', context)


def sign_up(request):
    if request.method == 'POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # check inputs
        if str(password1) != str(password2) and password1 < 8:
            print(
                "error:enter the password correctly or must contain atleast 8 character")
            return render(request, 'sign_up.html')

        if len(username) < 2:
            print("error:must be grater than 2 letter")
            return render(request, 'sign_up.html')

        if not username.isalnum:
            print("error:must be number and letters only")
            return render(request, 'sign_up.html')

        # creating user
        # import user
        try:
            users = User.objects.create_user(username, email, password1)
            users.first_name = fname
            users.last_name = lname
            users.save()
        except Exception as e:
            print("username already taken")
            return render(request, 'sign_up.html')

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


@login_required
def log_out(request):

    logout(request)
    print("logedohgcalhv")

    return redirect('home')


@login_required
def add(request):
    if request.method == "POST" and request.FILES['image_file']:
        user = request.user
        fullname = request.POST['fullname']
        address = request.POST['address'].capitalize()
        phone = request.POST['phone']
        about = request.POST['about']
        Type = request.POST['type']
        quantity = request.POST['quantity']
        price = request.POST['price']

        latitude = request.POST['latitude']
        longitude = request.POST['longitude']

        # handling date
        tz_ktm = pytz.timezone('Asia/Kathmandu')
        now = datetime.now(tz_ktm)
        now = str(now).split(" ")
        date = now[0]
        # --

        # handling image
        image_file = request.FILES['image_file']
        fs = FileSystemStorage(location='media/images/land_images/')
        # processing image
        # todo (275, 183)
        # --
        image_name = fs.save(image_file.name, image_file)
        # ---
        instance = Dhani(User=user, fullname=fullname, address=address, phone_number=phone,
                         about=about, latitude=latitude, longitude=longitude, landimage=image_file, Type=Type, quantity=quantity, price=price, created_at=date)
        instance.save()
        print("saved")

        return redirect('/')
    return render(request, 'add_post.html')


def make_map(coordinate):
    map = folium.Map(location=coordinate, tiles='OpenStreetMap',
                     zoom_start=15, width='100%', height='100%')

    folium.Marker(coordinate, popup='lmao', tooltip="click").add_to(map)

    # rendering map html
    map = map._repr_html_()
    return map


def map(request, pk):
    coordinate = Dhani.objects.get(pk=pk)

    m = make_map([coordinate.latitude, coordinate.longitude])
    return render(request, 'map.html', {"m": m})


@login_required
def usercomments(request, pk):

    if request.method == 'POST':

        comment = request.POST['comment']
        user = request.user
        comment_id = request.POST.get('commentid')
        post = Dhani.objects.get(pk=pk)
        parent = 'gg only for replies'

        instance = UserComments(Comments=comment, User=user, post=post)
        instance.save()
        print('comment sucessfully')

    post = Dhani.objects.get(pk=pk)
    context = {
        'comments': UserComments.objects.filter(post=post).order_by('-userid')
    }
    return render(request, 'comments.html', context)


@login_required
def update_post(request, pk):
    post = Dhani.objects.get(Userid=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            print('updated')

            return redirect('dashboard')

    context = {
        "form": form
    }

    return render(request, 'update_post.html', context)


@login_required
def dashboard(request):

    dashboardposts = Dhani.objects.all().filter(User=request.user)
    context = {
        "dashboardposts": dashboardposts
    }
    return render(request, 'dashboard.html', context)


@login_required
def delete_post(request, pk):
    post = Dhani.objects.get(Userid=pk)
    if request.method == 'POST':
        post.delete()
        print('deleted')
        return redirect('dashboard')
    return render(request, 'delete_post.html')


def howto(request):
    return render(request, 'how_to_use.html')


def allmap(request):
    obj = Dhani.objects.all()
    map = folium.Map(location=[obj[0].latitude, obj[0].longitude], tiles='OpenStreetMap',
                     zoom_start=15, width='100%', height='100%')
    for coordinate in obj:
        point = [coordinate.latitude, coordinate.longitude]
        folium.Marker(point).add_to(map)

    # rendering map html
    map = map._repr_html_()
    return render(request, 'map.html', {'m': map})
