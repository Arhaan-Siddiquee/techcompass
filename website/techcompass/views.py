from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
def home_view(request):
	# Add your view logic here
	return render(request, 'pages/home.html')

def roadmap_view(request):
	# Add your view logic here
	return render(request, 'pages/roadmaps.html')

def login_user(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/', {'success': 'You have been logged in'})
		else:
			messages.error(request, ('Invalid username or password'))
			return redirect('/login')
	else:
		return render(request, 'pages/login.html')
	
def logout_user(request):
	logout(request)
	messages.success(request, ('You have been logged out'))
	return redirect('/')

def register_user(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		try:
			user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
			user.save()
		except Exception as e:
			return render(request, 'pages/register.html', {'error': str(e)})
		login(request, user)
		return redirect('/')	
	else:
		return render(request, 'pages/register.html')

@login_required(login_url='/login')
def frontend_view(request):

	return render(request, 'pages/frontend.html')

@login_required(login_url='/login')
def backend_view(request):
	return render(request, 'pages/backend.html')

@login_required(login_url='/login')
def aiml_view(request):
		
	return render(request, 'pages/aiml.html')

@login_required(login_url='/login')
def blockchain_view(request):
	
	return render(request, 'pages/blockchn.html')

@login_required(login_url='/login')
def cybersec_view(request):
	
	return render(request, 'pages/cybersec.html')

@login_required(login_url='/login')
def dsa_view(request):
		
	return render(request, 'pages/dsa.html')

@login_required(login_url='/login')
def devops_view(request):
		
	return render(request, 'pages/devops.html')

@login_required(login_url='/login')
def datasci_view(request):

	return render(request, 'pages/datasci.html')

@login_required(login_url='/login')
def datanalyst_view(request):

	return render(request, 'pages/dataanalys.html')

@login_required(login_url='/login')
def dashboard_view(request):

	return render(request, 'pages/dashboard.html')