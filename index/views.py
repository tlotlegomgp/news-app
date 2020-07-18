from django.shortcuts import render, redirect
from . forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import requests
import os
from datetime import datetime, timedelta
from dateutil import tz

# Create your views here.

def convert_from_utc_to_local_time(date_time):

    utc_zone = tz.tzutc()

    utc = datetime.strptime(date_time,"%Y-%m-%dT%H:%M:%SZ")
    utc = utc.replace(tzinfo=utc_zone)
    central = utc + timedelta(hours = 2)
    localtime = central.strftime("%Y-%b-%d %H:%M%p")
    return localtime


def index_page(request):
    context = {}
    API_KEY = os.environ.get('NEWSAPI_KEY')
    headlines_url = 'http://newsapi.org/v2/top-headlines?''country=za&''pageSize=100&''apiKey={}'
    query_url = 'https://newsapi.org/v2/everything?q={}&sortBy=publishedAt&language=en&apiKey={}'

    if request.method == "GET" and 'q' in request.GET:

        if request.user.is_authenticated:
            query = request.GET['q']
        else:
            return redirect('login')

        response = requests.get(query_url.format(query, API_KEY)).json()

        if response['totalResults'] == 0:
            context['error_report'] = "The query you made brought no matching results."
            context['query'] = query

        else:
            #Convert timezones from UTC to localtime and format the datetime outputs
            for a in response['articles']:
                a['publishedAt'] = convert_from_utc_to_local_time(a['publishedAt'])

            context['articles'] = response['articles']

    else:
        form = RegisterForm()
        context['form'] = form
        response = requests.get(headlines_url.format(API_KEY)).json()

        #Convert timezones from UTC to localtime and format the datetime output
        for a in response['articles']:
            a['publishedAt'] = convert_from_utc_to_local_time(a['publishedAt'])

        context['articles'] = response['articles']

    return render(request, 'index/index.html', context)


def register_view(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            if User.objects.filter(username = username).exists():
                messages.error(request,'Username, ' + username + ', is already in use.')
            else:
                user = User.objects.create_user(username = username, password = password)
                user.save()
                login(request, user)
                return redirect('home_page')

    else:
        form = RegisterForm()

    return render(request, 'index/register.html', {'form': form})


def login_view(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home_page')
            else:
                messages.error(request,'Username or Password entered incorrect.')
            
            
    else:
        form = RegisterForm()
        
    return render(request, 'index/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home_page')