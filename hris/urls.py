from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_home, name='redirect_home'),

    path('projects', views.projects, name='projects'),
    path('add_project', views.add_project, name='add_project'),
    path('view_project_details/<int:pk>/', views.view_project_details, name='view_project_details'),
    path('update_project/<int:pk>', views.update_project, name='update_project'),

    path('workers', views.workers, name='workers'),
    path('add_worker', views.add_worker, name='add_worker'),
    path('worker_details/<int:pk>', views.worker_details, name='worker_details'),
    path('delete_worker/<int:pk>', views.delete_worker, name='delete_worker'),
    path('update_worker/<int:pk>', views.update_worker, name='update_worker'),

    path('add_applicant/<int:project_pk>', views.add_applicant, name='add_applicant'),
    path('view_applicant/<int:pk>', views.view_applicant, name='view_applicant'),
    path('update_applicant/<int:pk>', views.update_applicant, name='update_applicant'),
    path('unassign_applicant/<int:pk>', views.unassign_applicant, name='unassign_applicant'),
    path('add_eval/<int:applicant_pk>', views.add_eval, name='add_eval'),
    path('update_eval/<int:pk>', views.update_eval, name='update_eval'),

    path('users', views.users, name='users'),
    path('add_users', views.add_users, name='add_users'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout')
]