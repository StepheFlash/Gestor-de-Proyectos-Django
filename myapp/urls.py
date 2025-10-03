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
    path('content/approach_project/', views.content_approach_project, name='content_approach_project'),
    path('content/planning_project/', views.content_planning_project, name='content_planning_project'),
    path('content/systemic_review/', views.content_systemic_review, name='content_systemic_review'),
    path('content/validation/', views.content_validation, name='content_validation'),
    path('content/subtantiation/', views.content_subtantiation, name='content_subtantiation'),
    path('content/activity/<int:id_activity>/multimedia/detail', views.content_guide_detail,name='content_guide_detail'),
    path('projects/', views.projects, name='projects'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/assing/members', views.assing_members_project, name="assing_members_project"),
    path('integrantes/ajax-detalle/', views.integrante_ajax_detalle, name="integrante_ajax_detalle"),
    path('projects/json/', views.projects_json, name='projects_json'),
    path('projects/<int:id>/detail', views.project_detail, name='project_detail'),
    path('projects/<int:id>/info/general', views.project_info, name='project_info'),
    path('projects/<int:id>/edit', views.project_edit, name='project_edit'),
    path('projects/create/document/', views.create_document_project, name='create_document_project'),
    path('projects/<int:id_document>/edit/document/', views.project_document_edit, name='project_document_edit'),
    path('projects/<int:id_document>/detail/document/', views.project_document_detail, name='project_document_detail'),
    path('projects/<int:id>/info/general/activity/<int:id_activity>/tasks',views.project_activities_tasks, name='project_activities_tasks'),
    path('activities/',views.activities, name='activities'),
    path('activities/list/',views.activities_list, name='activities_list'),
    path('activities/list/json/',views.activities_json, name='activities_json'),
    path('activities/create',views.activity_create, name="activity_create"),
    path('activities/<int:id_activity>/edit',views.activity_edit, name="activity_edit"),
    path('activities/<int:id_activity>/delete',views.activity_delete, name="activity_delete"),
    path('activity/<int:id_activity>/resources/view',views.activity_resources, name="activity_resources"),
    path('activity/<int:id_activity>/resources/list',views.resources_json, name="resources_json"),
    path('activity_resources_add/',views.activity_resources_add, name="activity_resources_add"),
    path('activity_resources/<int:id_resource>/edit',views.activity_resources_edit,name="activity_resources_edit"),
    path('activity_resources/<int:id_resource>/detail',views.activity_resources_detail,name="activity_resources_detail"),
    path('projects/info/general/activity/tasks/create', views.create_task_project, name='create_task_project'),
    path('tasks_feedback/<int:id_task>/add', views.task_feedback, name="task_feedback"),
    path('tasks/<int:id_task>/edit', views.task_edit, name="task_edit"),
    path('task/<int:task_id>/detail', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('task/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('calendar/view/', views.calendar, name = 'calendar'),
    path('calendar/create_event/', views.calendar_create_event, name = 'calendar_create_event'),
    path('calendar/<int:id_meeting>/event/detail/', views.calendar_event_detatils, name='calendar_event_detatils'),
    path('calendar/<int:id_meeting>/create_note/', views.calendar_create_note, name = 'calendar_create_note'),
    path('calendar/<int:id_meeting>/event_into/', views.calendar_event_info, name='calendar_event_info'),
    path('calendar/<int:id_meeting>/event_edit/', views.calendar_event_edit, name='calendar_event_edit'),
    path('calendar/event_json/',views.calendar_event_json, name='calendar_event_json'),
    path('calendar/<int:id_meeting>/event_delete/', views.calendar_event_delete, name='calendar_event_delete'),

    #path('tasks/<int:id_task>/status_update/', views.task_status_update, name='task_status_update'),
    #path('create_project/', views.create_project, name='create_project'),
]