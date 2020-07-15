from django.shortcuts import render, redirect
from . forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import requests
import os
from datetime import datetime
from dateutil import tz

# Create your views here.

def convert_from_uct_to_local_time(date_time):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    utc = datetime.strptime(date_time,"%Y-%m-%dT%H:%M:%SZ")
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    localtime = central.strftime("%Y-%b-%d %H:%M%p")
    return localtime

def index_page(request):
    context = {}
    API_KEY = os.environ.get('NEWSAPI_KEY')
    headlines_url = 'http://newsapi.org/v2/top-headlines?''country=za&''pageSize=100&''apiKey={}'
    query_url = 'https://newsapi.org/v2/everything?q={}&sortBy=publishedAt&apiKey={}'

    if request.method == "POST":
        form = RegisterForm(request.POST)
        context['form'] = form
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

    elif request.method == "GET" and 'q' in request.GET:

        query = request.GET['q']
        response = requests.get(query_url.format(query, API_KEY)).json()

        if response['totalResults'] == 0:
            context['error_report'] = "The query you made brought no matching results."
            context['query'] = query

        else:
            #Convert timezones from UTC to localtime and format the datetime output
            for a in response['articles']:
                a['publishedAt'] = convert_from_uct_to_local_time(a['publishedAt'])

            context['articles'] = response['articles']

    else:
        form = RegisterForm()
        context['form'] = form
        response = requests.get(headlines_url.format(API_KEY)).json()

        #Convert timezones from UTC to localtime and format the datetime output
        for a in response['articles']:
            a['publishedAt'] = convert_from_uct_to_local_time(a['publishedAt'])

        context['articles'] = response['articles']

    return render(request, 'index/index.html', context)


def logout_view(request):
    logout(request)
    return redirect('home_page')