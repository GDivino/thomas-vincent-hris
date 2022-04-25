from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('projects', views.projects, name='projects'),
    path('add_project', views.add_project, name='add_project'),
    path('view_project_details/<int:pk>/', views.view_project_details, name='view_project_details'),
]