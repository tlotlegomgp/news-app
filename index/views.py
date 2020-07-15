from django.shortcuts import render
from . forms import RegisterForm
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
    if request.method == "POST":
        form = RegisterForm(request.POST)
        context['form'] = form
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

        else:
            pass 
    else:
        form = RegisterForm()
        context['form'] = form
        API_KEY = os.environ.get('NEWSAPI_KEY')
        url = ('http://newsapi.org/v2/top-headlines?''country=za&''pageSize=100&''apiKey={}')
        response = requests.get(url.format(API_KEY)).json()

        #Convert timezones from UTC to localtime and format the datetime output
        for a in response['articles']:
            a['publishedAt'] = convert_from_uct_to_local_time(a['publishedAt'])

        context['articles'] = response['articles']

    return render(request, 'index/index.html', context)