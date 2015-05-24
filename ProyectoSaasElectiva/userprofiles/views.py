from django.shortcuts import render

# Create your views here.
# importamos el formulario que creamos en froms.py
from .forms import UserCreationEmailForm

def signup(request):
	form = UserCreationEmailForm()

	return render(request, 'signup.html', {'form':form})
