from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/create/', views.project_create, name='project_create'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('project/<int:project_pk>/task/create/', views.task_create, name='task_create'),
    path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:pk>/update-status/', views.update_task_status, name='update_task_status'),
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
]