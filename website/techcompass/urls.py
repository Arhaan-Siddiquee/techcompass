from django.urls import path
from . import views

app_name = "techcompass"

#URLconfig
urlpatterns = [
    path('', views.home_view, name='index'),
    path('roadmap', views.roadmap_view, name='roadmap'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    
]