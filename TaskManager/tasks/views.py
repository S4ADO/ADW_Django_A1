from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

def index(request):
	form = AuthenticationForm()
	return render(request, 'signin.html', {'form': form})

def home(request):
	return render(request, 'home.html', context = None)

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return render(request, 'home.html', context = None)
	else:
		form = UserCreationForm()
	return render(request, 'register.html', {'form': form})

def signin(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active == 1:
					request.session.set_expiry(86400) #sets the exp. value of the session 
					login(request, user)
					return render(request, 'home.html', context = None)
	else:
		form = AuthenticationForm()
	return render(request, 'signin.html', {'form': form})	

def logout(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('home')
	else:
		form = UserCreationForm()
	return render(request, 'register.html', {'form': form})	
