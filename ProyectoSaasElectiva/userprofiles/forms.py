from django import forms
#importamos de los formulacios de django uno que me permita crear usuarios
from django.contrib.auth.forms  import UserCreationForm
# improtamos modelo usuarios
from django.contrib.auth.models import User

class UserCreationEmailForm(UserCreationForm):
	email = forms.EmailField()
	# sobre escribimos los campos por defecto y agregamos Email
	class Meta:
		model = User
		fields = ('username','email')
