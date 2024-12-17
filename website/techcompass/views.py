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
from .models import Roadmap, Progress, Course
from django.utils import timezone
from django.core.exceptions import ValidationError
import json




# Create your views here.
def home_view(request):
	# Add your view logic here
	return render(request, 'pages/home.html')

def roadmap_view(request):
	roadmap = Roadmap.objects.all()
	return render(request, 'pages/roadmaps.html', {'roadmaps': roadmap})

@login_required(login_url='/login')
def roadmap_detail_view(request, roadmap_name):
	if request.method == "GET":
		if not Roadmap.objects.filter(title=roadmap_name).exists():
			return HttpResponse(f"Roadmap named: {roadmap_name} not found", status=404)
		roadmap = Roadmap.objects.get(title=roadmap_name)
		courses = roadmap.courses_provided.all()
		completed = Progress.objects.filter(user=request.user, roadmap=roadmap, completed=True)
		p =[]
		inprogress_roadmaps = request.user.progress.filter(completed=False)
		for i in inprogress_roadmaps:
			courses_completed = i.completed_courses.all()
			courses_provided = i.roadmap.courses_provided.all()
			p.append((i,f"{len(courses_completed)/len(courses_provided)*100:.0f}"))
		try:
			progress = Progress.objects.get(user=request.user, roadmap=roadmap)
		except Progress.DoesNotExist:
			return render(request, 'pages/roadmap_detail.html', {'roadmap': roadmap, 'courses': courses,"not_registered":True,'media_url': settings.MEDIA_URL})
		
		completed_courses = progress.completed_courses.all()
		return render(request, 'pages/roadmap_detail.html', {'roadmap': roadmap, 'courses': courses, 'completed_courses': completed_courses,"finished":completed,'in_progress': p,'media_url': settings.MEDIA_URL})
	else:
		return JsonResponse({'error': 'Invalid request'})
	

@login_required(login_url='/login')
def roadmap_register_view(request, roadmap_name):
	if not Roadmap.objects.filter(title=roadmap_name).exists():
		return HttpResponse(f"Roadmap named: {roadmap_name} not found", status=404)
	roadmap = Roadmap.objects.get(title=roadmap_name)
	try:
		progress = Progress.objects.get(user=request.user, roadmap=roadmap)
	except Progress.DoesNotExist:
		progress = Progress(user=request.user, roadmap=roadmap)
		progress.save()
	return redirect(f'/roadmap/{roadmap_name}')

@login_required(login_url='/login')
def course_update_view(request):
	if request.method == "POST":
		print(request.body)
		body = json.loads(request.body)
		course_title = body['course_title']
		roadmap_id = body['roadmap_id']
		is_checked= body['is_checked']
		print(course_title, roadmap_id, is_checked)
		roadmap = Roadmap.objects.get(id=roadmap_id)
		course = Course.objects.get(title=course_title)
		progress = Progress.objects.get(user=request.user, roadmap=roadmap)
		if is_checked:
			progress.completed_courses.add(course)
			if progress.completed_courses.count() == roadmap.courses_provided.count():
				progress.completed = True
				progress.completed_at = timezone.now()
				progress.save()
			return JsonResponse({'success': 'Course completed'})
		else:
			progress.completed_courses.remove(course)
			progress.completed = False
			progress.completed_at = None
			progress.save()
			return JsonResponse({'success': 'Course not completed'})
	else:
		return JsonResponse({'error': 'Invalid request'})

def login_user(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ('You have been logged in'))
			return redirect('/dashboard')
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
			if 'UNIQUE constraint' in str(e):
				messages.error(request, ('Username already exists'))
			#elif 'password does not match' in str(e):
			else:
				messages.error(request, ('Invalid username or password'))
			return render(request, 'pages/register.html')
		login(request, user)
		return redirect('/dashboard')	
	else:
		return render(request, 'pages/register.html')

@login_required(login_url='/login')
def frontend_view(request):

	return render(request, 'pages/frontend.html',{'roadmaps': request.user.roadmaps.all()})


@login_required(login_url='/login')
def dashboard_view(request,success=False):
	completed_roadmaps = request.user.progress.filter(completed=True)
	inprogress_roadmaps = request.user.progress.filter(completed=False)
	p =[]
	for i in inprogress_roadmaps:
		courses_completed = i.completed_courses.all()
		courses_provided = i.roadmap.courses_provided.all()
		p.append((i,f"{len(courses_completed)/len(courses_provided)*100:.0f}"))
	return render(request, 'pages/dashboard.html',{'user': request.user, 'in_progress': p,
	'completed_roadmaps': completed_roadmaps, 'media_url': settings.MEDIA_URL,"success":success})