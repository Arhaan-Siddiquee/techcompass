from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .forms import SignUpForm
from django import forms
from django.http import HttpResponse


# Create your views here.
def home_view(request):
	# Add your view logic here
	return render(request, 'pages/home.html')

def roadmap_view(request):
	# Add your view logic here
	return render(request, 'pages/roadmaps.html')

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ('You have been logged in'))
			return redirect('/')
		else:
			messages.error(request, ('Invalid username or password'))
			return redirect('/login')
	else:
		return render(request, 'pages/login.html')
	
def logout_user(request):
	logout(request)
	messages.success(request, ('You have been logged out'))
	return redirect('/')