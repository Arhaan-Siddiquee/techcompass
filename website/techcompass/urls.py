from django.urls import path
from . import views

app_name = "techcompass"

#URLconfig
urlpatterns = [
    path('', views.home_view, name='index'),
    path('roadmap', views.roadmap_view, name='roadmap'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    # path('reset_password', views.reset_password, name='reset_password'),
    path('register', views.register_user, name='register'),
    path('frontend', views.frontend_view, name='frontend'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('roadmap/<str:roadmap_name>', views.roadmap_detail_view, name='roadmap_detail'),
    path('course_update', views.course_update_view, name='course_update'),
    path('roadmap_register/<str:roadmap_name>', views.roadmap_register_view, name='roadmap_register'),
    
]