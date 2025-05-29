from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('inicio/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('login/', views.inicio_sesion, name='login'),
    path('projects/', views.projects, name='projects'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:id>', views.project_detail, name='project_detail'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('task/create/', views.create_task, name='create_task'),
    path('task/<int:task_id>/detail', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('task/<int:task_id>/delete', views.delete_task, name='delete_task'),
    # path('create_project/', views.create_project, name='create_project'),
]