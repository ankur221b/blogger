from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import pymongo
import json
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.template import Context
from bs4 import BeautifulSoup
import datetime

myclient = pymongo.MongoClient(
    "mongodb://ank:ank@blogdb-shard-00-00-jxlkt.mongodb.net:27017,blogdb-shard-00-01-jxlkt.mongodb.net:27017,blogdb-shard-00-02-jxlkt.mongodb.net:27017/test?ssl=true&replicaSet=blogdb-shard-0&authSource=admin&retryWrites=true&w=majority")
mydb = myclient["blogdb"]
col = mydb["blog"]

month = ['January', 'Feburary', 'March', 'April',
         'May', 'June', 'July', 'August', 'September',
                'October', 'November', 'December']

# Create your views here.


def home(request):
    background = 'https://docs.google.com/uc?export=download&id=1H1UB9ysxpwBPEsbSUhdzjw1x4Fvc6o92'

    context = {}
    context['background'] = background
    posts = col.find().sort([('date', -1), ('time', -1)])
    context['posts'] = posts

    return render(request, 'home.html', context)


def search(request):

    background = 'https://docs.google.com/uc?export=download&id=1H1UB9ysxpwBPEsbSUhdzjw1x4Fvc6o92'
    context = {}

    if request.GET:
        search_term = request.GET['search_term']
        posts = col.find({'title': {'$regex': search_term, '$options': 'i'}})
        context['posts'] = posts
        context['background'] = background

        return render(request, 'home.html', context)

    redirect('home')


@csrf_exempt
@login_required
def edit(request, title):

    posts = col.find_one({'title': title})
    #cleantext = BeautifulSoup(posts['post'], "html.parser").text
    cleantext = posts['post']
    context = {}

    context['post'] = cleantext
    context['title'] = title

    return render(request, 'forms.html', context)


@login_required
def make_edit(request, title):

    if request.POST:
        col.update_one({'title': title},
                       {'$set': {'post': request.POST['post'],
                                 'title': request.POST['title']}})

    return redirect('home')


def post_view(request, title):
    posts = col.find_one({'title': title})
    context = {}
    background = 'https://docs.google.com/uc?export=download&id=1H1UB9ysxpwBPEsbSUhdzjw1x4Fvc6o92'
    context['background'] = background
    context['posts'] = posts

    return render(request, 'post.html', context)


@csrf_exempt
def delete(request, title):
    col.delete_one({'title': title})
    return redirect('home')


@login_required
@csrf_exempt
def new_blog(request):

    if request.POST:

        post = request.POST['post']
        title = request.POST['title']
        context = {}
        context['post'] = post
        context['title'] = title
        context['user'] = request.user.username

        current_date = datetime.datetime.now()
        date = '{} {}, {}'.format(
            month[current_date.month - 1], current_date.day, current_date.year)
        context['date'] = date

        current_time = datetime.datetime.now()
        time = current_time.strftime("%H:%M:%S")
        context['time'] = time

        current_post = col.insert_one(context)

        return redirect('home')

    return render(request, 'editor.html')


@csrf_exempt
def login(request):

    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        username = request.POST.get('name')
        print(username)
        if username is None:
            username = User.objects.get(email=email.lower()).username
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                django_login(request, user)
                return redirect('home')
            else:
                return redirect('login')
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password)
            user.save()
            return redirect('home')

    else:
        return render(request, 'login.html')


def logout(request):
    django_logout(request)
    return redirect('home')


@login_required
def profile(request):
    return render(request, 'profile.html')
