from django.urls import path
from . import views

app_name = "techcompass"

#URLconfig
urlpatterns = [
    path('', views.home_view, name='index'),
    path('roadmap', views.roadmap_view, name='roadmap'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('frontend', views.frontend_view, name='frontend'),
    path('backend', views.backend_view, name='backend'),
    path('aiml', views.aiml_view, name='aiml'),
    path('blockchain', views.blockchain_view, name='blockchain'),
    path('cybersec', views.cybersec_view, name='cybersec'),
    path('dsa', views.dsa_view, name='dsa'),
    path('devops', views.devops_view, name='devops'),
    path('datasci', views.datasci_view, name='datasci'),
    path('datanalyst', views.datanalyst_view, name='datanalyst'),

    
]