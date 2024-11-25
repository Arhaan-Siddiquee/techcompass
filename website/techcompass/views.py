from django.shortcuts import render
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, JsonResponse



# Create your views here.
def home_view(request):
	# Add your view logic here
	return render(request, 'pages/home.html')