from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length = 30, widget=forms.TextInput(attrs={'class':"form-control", 'name':"username", 'required':"", 'placeholder':"Username"}))
    password = forms.CharField(max_length = 20, widget = forms.PasswordInput(attrs={'class':"form-control", 'name':"password", 'required':"", 'placeholder':"Password"}))