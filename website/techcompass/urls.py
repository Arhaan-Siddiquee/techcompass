from django.urls import path
from . import views

app_name = "techcompass"

#URLconfig
urlpatterns = [
    path('', views.home_view, name='index'),
    path('roadmap', views.roadmap_view, name='roadmap')

]