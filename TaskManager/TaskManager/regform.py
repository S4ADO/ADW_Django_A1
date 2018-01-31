from django import forms 
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class RegForm(forms.Form):
	username = forms.CharField(label='Username', max_length=50)
	email = forms.EmailField(label='Email')
	password = forms.CharField(label='Password', widget=forms.PasswordInput())
	passwordver = forms.CharField(label='Password (Again)', widget=forms.PasswordInput())

	def clean_password2(self):
	if 'password' in self.cleaned_data:
		password = self.cleaned_data['password']
		passwordver = self.cleaned_data['passwordver']
		if password == passwordver:
			return passwordver
		raise forms.ValidationError('Passowrds inputted do not match!')
		
	def clean_username(self):
		username = self.cleaned_data['username']
		if not re.search(r'^\w+$', username):
			raise forms.ValidationError('Username can only contain alphanumeric characters and underscores.')
		try:
			User.objects.get(username=username)
		except ObjectDoesNotExist:
			return username
		raise forms.ValidationError('Username is already taken.')	