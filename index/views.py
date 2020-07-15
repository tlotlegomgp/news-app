from django.shortcuts import render
from . forms import RegisterForm
import requests
import os

# Create your views here.

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
        context['articles'] = response['articles']

    return render(request, 'index/index.html', context)