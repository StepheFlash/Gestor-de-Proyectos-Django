from django.urls import path
"""
Configuración de URL para la aplicación Django.
Define los patrones de URL y sus funciones de vista correspondientes:
- '' : Página de inicio, gestionada por `views.home`, llamada 'home'.
- 'inicio/' : Página de índice, gestionada por `views.index`, llamada 'index'.
- 'about/' : Página "Acerca de", gestionada por `views.about`, llamada 'about'.
- 'registro/' : Registro de usuario, gestionado por `views.registro`, llamado 'registro'.
- 'logout/' : Cierre de sesión de usuario, gestionado por `views.cerrar_sesion`, llamado 'logout'.
- 'login/' : Inicio de sesión de usuario, gestionado por `views.inicio_sesion`, llamado 'login'.
- 'projects/' : Lista de proyectos, gestionada por `views.projects`, llamado 'projects'. - 'projects/create/': Crea un nuevo proyecto, gestionado por `views.create_project`, llamado 'create_project'.
- 'projects/<int:id>': Vista detallada del proyecto, gestionada por `views.project_detail`, llamada 'project_detail'.
- 'tasks/': Lista de tareas, gestionada por `views.tasks`, llamada 'tasks'.
- 'tasks_completed/': Lista de tareas completadas, gestionada por `views.tasks_completed`, llamada 'tasks_completed'.
- 'task/create/': Crea una nueva tarea, gestionada por `views.create_task`, llamada 'create_task'. - 'task/<int:task_id>/detail': Vista de detalle de la tarea, gestionada por `views.task_detail`, llamada 'task_detail'.
- 'task/<int:task_id>/complete': Marcar la tarea como completada, gestionada por `views.complete_task`, llamada 'complete_task'.
- 'task/<int:task_id>/delete': Eliminar una tarea, gestionada por `views.delete_task`, llamada 'delete_task'.
"""
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
    path('projects/assing/members', views.assing_members_project, name="assing_members_project"),
    path('integrantes/ajax-detalle/', views.integrante_ajax_detalle, name="integrante_ajax_detalle"),
    path('projects/<int:id>/detail', views.project_detail, name='project_detail'),
    path('projects/<int:id>/info/general', views.project_info, name='project_info'),
    path('projects/<int:id>/edit', views.project_edit, name='project_edit'),
    path('projects/approach/', views.approach_project, name='approach_project'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('task/create/', views.create_task, name='create_task'),
    path('task/<int:task_id>/detail', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('task/<int:task_id>/delete', views.delete_task, name='delete_task'),
    # path('create_project/', views.create_project, name='create_project'),
]