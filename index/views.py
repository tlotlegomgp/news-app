from django.shortcuts import render
from . forms import RegisterForm

# Create your views here.

def index_page(request):
    #If user has filled the email form and wants to post form
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]

            #Process Create User

	#Else Present empty form to user
	else:
		form = RegisterForm()
		
	return render(request, 'index/index.html', {'form': form})
	
