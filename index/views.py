from django.shortcuts import render
from . forms import RegisterForm
import requests
import os

# Create your views here.

def index_page(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

        else:
            pass 
    else:
        form = RegisterForm()
        API_KEY = os.environ.get('NEWSAPI_KEY')
        url = ('http://newsapi.org/v2/top-headlines?''country=za&''apiKey={}')
        response = requests.get(url.format(API_KEY)).json()
            
        print(response)

    return render(request, 'index/index.html', {'form' : form})