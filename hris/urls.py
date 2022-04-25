from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('projects', views.projects, name='projects'),
    path('add_project', views.add_project, name='add_project'),
    path('view_project_details/<int:pk>/', views.view_project_details, name='view_project_details'),

    path('workers', views.workers, name='workers'),
    path('add_worker', views.add_worker, name='add_worker'),
    path('worker_details/<int:pk>', views.worker_details, name='worker_details'),
    path('delete_worker/<int:pk>', views.delete_worker, name='delete_worker'),
    path('update_worker/<int:pk>', views.update_worker, name='update_worker')
]