from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings



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
			return redirect('/dashboard', {'success': 'You have been logged in'})
		else:
			messages.error(request, ('Invalid username or password'))
			return redirect('/login')
	else:
		return render(request, 'pages/login.html')
	
# def reset_password(request):
# 	return render(request, 'pages/reset_password.html')

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
		return redirect('/dashboard')	
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
	completed_roadmaps = request.user.progress.filter(completed=True)
	inprogress_roadmaps = request.user.progress.filter(completed=False)
	print(inprogress_roadmaps)
	p =[]
	for i in inprogress_roadmaps:
		courses_completed = i.completed_courses.all()
		courses_provided = i.roadmap.courses_provided.all()
		p.append((i,f"{len(courses_completed)/len(courses_provided)*100:.0f}"))
	return render(request, 'pages/dashboard.html',{'user': request.user, 'in_progress': p,
	'completed_roadmaps': completed_roadmaps, 'media_url': settings.MEDIA_URL})