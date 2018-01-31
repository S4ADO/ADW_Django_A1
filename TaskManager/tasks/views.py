from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.http import HttpResponse
from .forms import UserForm

def index(request):
    return render(request, 'login.html', context = None)

def register(request):
    return HttpResponse("register")

class UserFormView(View):
	formc = UserForm
	templaten = 'tasks/register.html'

	#Display reg form
	def get(self, request):
		form = self.formc(None)
		return render(request, self.templaten, {'form': form})

	#Handle register request
	def post(self, request):
		form = self.formc(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()