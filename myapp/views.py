
"""
Vistas de Django para autenticación de usuarios, gestión de proyectos y tareas.
Functions:
    home(request):
        Renderizar la página de inicio.
    registro(request):
        Gestionar el registro de usuarios. En GET, mostrar el formulario de registro. En POST, crear un usuario si las contraseñas coinciden.
    inicio_sesion(request):
        Gestionar el inicio de sesión del usuario. En GET, mostrar el formulario de inicio de sesión. En POST, autenticar e iniciar sesión del usuario.
   cerrar_sesion(request):
        Cerrar la sesión del usuario actual y redirigir a la página de inicio de sesión.
    index(request):
        Mostrar la página de índice principal para los usuarios conectados, mostrando la información del usuario.
    projects(request):
        Mostrar una lista de todos los proyectos.
    about(request):
        Mostrar la página "Acerca de".
    tasks(request):
        Mostrar una lista de tareas incompletas para el usuario conectado.
    tasks_completed(request):
        Mostrar una lista de tareas completadas para el usuario conectado.
    create_task(request):
        Gestionar la creación de una nueva tarea. En GET, mostrar el formulario de creación de tareas. En POST, crear la tarea.
    task_detail(request, task_id):
        Mostrar y actualizar los detalles de una tarea específica perteneciente al usuario conectado.
    complete_task(request, task_id):
        Marcar una tarea específica como completada para el usuario conectado.
    delete_task(request, task_id):
        Elimina una tarea específica del usuario conectado.
    create_project(request):
        Gestiona la creación de un nuevo proyecto. En GET, muestra el formulario de creación del proyecto. En POST, crea el proyecto.
    project_detail(request, id):
        Muestra los detalles y las tareas asociadas a un proyecto específico.
"""
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
# from .forms import TaskForm, CreateNewProject
from .models import Project, Task, Studentuser, Metting, Stage, Activity, Document
from django.utils import timezone
from datetime import datetime
import json
from django.urls import reverse



# Create your views here.


def home(request):
    return render(request, 'home.html')


def registro(request):

    if request.method == 'GET':
        return render(request, 'registro.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    first_name=request.POST['firstname'],
                    last_name=request.POST['lastname'],
                    email=request.POST['email'],
                    password=request.POST['password1']
                )
                user.save()
                integrante = Studentuser.objects.create(
                    user=user,
                    project_id=None,
                    cedula=request.POST['cedula'],
                    student_code=request.POST['student_code']
                )
                integrante.save()
                # Funcion para almacenar la sesion del usuario
                login(request, user)
                return redirect('login')
            except IntegrityError:
                return render(request, 'registro.html', {
                    'form': UserCreationForm,
                    'error': 'Error al crear el usuario: ya existe'
                })
        else:
            return render(request, 'registro.html', {
                'form': UserCreationForm,
                'error': 'Las contraseñas no coinciden'
            })


def inicio_sesion(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'Usuario y/o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('index')


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('login')


@login_required
def user_data(request):
    usuario = request.user
    nombre_completo = usuario.first_name + ' ' + usuario.last_name
    email = usuario.email
    data_user = {
        'nombre_completo': nombre_completo,
        'email': email,
    }

    return data_user


@login_required
def index(request):
    title = ' !Hola, Bienvenido a la App de Django!'
    data_user = user_data(request)
    return render(request, 'index.html', {'title': title, 'data_user': data_user})


def about(request):
    return render(request, 'about.html')

# Funtion ...


@login_required
def projects(request):
    # projects = list(Proyect.objects.values())
    projects = Project.objects.all()
    integrantes = Studentuser.objects.select_related('user').all()
    # return JsonResponse(projects, safe=False)
    data_user = user_data(request)
    return render(request, 'projects/projects.html', {'projects': projects, 'data_user': data_user, 'integrantes': integrantes})


@login_required
def create_project(request):
    if request.method == 'GET':
        return render(request, 'projects/create_project.html')
    else:
        try:
            Project.objects.create(
                name=request.POST.get("name", "").strip(),
                horario_reunion=request.POST.get(
                    "horario_reunion", "").strip(),
                tema_investigacion=request.POST.get(
                    "tema_investigacion", "").strip()
            )
            return redirect('projects')
        except Exception as e:
            return render(request, 'projects/projects.html', {
                'error': 'Por favor introduzca datos válidos',
                'exception': str(e)
            })


@login_required
def create_document_project(request):
    if request.method == 'GET':
        return render(request, 'projects/documents/document_add.html')
    else:
        project_id = request.POST.get("id_project_doc")
        Document.objects.create(
            project_id=project_id,
            title_doc=request.POST.get("title_doc"),
            content_doc=request.POST.get("content_doc"),
            date_uploaded=request.POST.get("date_uploaded"),
            upload_path=request.POST.get("upload_path")

        )
        return redirect('project_info', id=project_id)


@login_required
def assing_members_project(request):
    integrantes = Studentuser.objects.select_related('user').all()
    if request.method == 'GET':
        return render(request, 'projects/project_members.html', {'integrantes': integrantes})
    elif request.method == 'POST':
        integrante_id = request.POST.get('integranteSelect')
        project_id = request.POST.get('project_id')

        if not integrante_id or not project_id:
            return HttpResponseBadRequest("Faltan datos.")

        integrante = get_object_or_404(Studentuser, pk=integrante_id)
        integrante.project_id = project_id
        integrante.save()

        return redirect('projects')
    else:
        return HttpResponseBadRequest("Metodo no permitido")


@login_required
def integrante_ajax_detalle(request):
    integrante_id = request.GET.get('integrante_id')
    # print("integrante_id",integrante_id)
    integrante = get_object_or_404(Studentuser, id=integrante_id)

    data = {
        'cedula': integrante.cedula,
        'student_code': integrante.student_code,
        'institutional_mail': integrante.user.email
    }
    return JsonResponse(data)


@login_required
def project_info(request, id):
    project = get_object_or_404(Project, pk=id)
    integrantes = Studentuser.objects.select_related(
        'user').filter(project_id=id)
    stages = Stage.objects.all()
    activities = Activity.objects.all()
    documents = Document.objects.filter(project_id=id)
    return render(request, 'projects/project_info.html',
                  {
                      'project': project,
                      'integrantes': integrantes,
                      'stages': stages,
                      'activities': activities,
                      'documents': documents
                  })


@login_required
def approach_project(request):
    return render(request, 'projects/approach/project_approach.html')


@login_required
def activities(request):
    activity_planteamiento = Activity.objects.filter(etapa_id=1)
    activity_planificacion = Activity.objects.filter(etapa_id=2)
    #activity_ejecucion = Activity.objects.filter(etapa_id=3)
    #activity_desarrollo = Activity.objects.filter(etapa_id=4)

    return render(request, 'tasks/activities/activities.html', {
        'activity_planteamiento': activity_planteamiento,
        'activity_planificacion': activity_planificacion,
        #'activity_ejecucion': activity_ejecucion,
        #'activity_desarrollo': activity_desarrollo
    })


@login_required
def project_activities_tasks(request, id, id_activity):
    project = get_object_or_404(Project, pk=id)
    activity = get_object_or_404(Activity, pk=id_activity)
    tasks = Task.objects.filter(activity_id=id_activity, project_id=id)
    documents = Document.objects.filter(project_id=id)
    if request.method == 'GET':
        return render(request, 'tasks/activities/activities_view.html', {
            'project': project,
            'activity': activity,
            'tasks': tasks,
            'documents': documents
        })


@login_required
def tasks_detail(request):
    print("listar tareas")


@login_required
def tasks_completed(request):
    TaskCompleted = "Tareas Completadas"
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks/tasks.html', {'tasks': tasks, 'TaskCompleted': TaskCompleted})


@login_required
def create_task_project(request):

    if request.method == 'GET':
        return render(request, 'tasks/create_task.html')

    else:
        project_data_id = request.POST.get("id_project")
        activity_data_id = request.POST.get("id_activity")

        Task.objects.create(
            project_id=project_data_id,
            activity_id=activity_data_id,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            document_id=request.POST.get("documentSelect", ""),
            important=bool(request.POST.get("important"))

        )
        return redirect('project_activities_tasks', project_data_id, activity_data_id)


@login_required
# Pendiente editarlo
def project_edit(request, id):
    project = get_object_or_404(Project, pk=id)
    integrantes = Studentuser.objects.select_related(
        'user').filter(project=project)
    if request.method == 'GET':
        return render(request, 'projects/project_edit.html', {
            'project': project,
            'integrantes': integrantes
        })
    else:
        try:
            project.name = request.POST.get('name')
            project.horario_reunion = request.POST.get('horario_reunion')
            project.tema_investigacion = request.POST.get('tema_investigacion')
            project.save()

            for integrante in integrantes:
                integrante.user.first_name = request.POST.get(
                    f'integrante_first_name_{integrante.id}')
                integrante.user.last_name = request.POST.get(
                    f'integrante_last_name_{integrante.id}')
                integrante.cedula = request.POST.get(f'cedula_{integrante.id}')
                integrante.student_code = request.POST.get(
                    f'student_code_{integrante.id}')
                integrante.user.email = request.POST.get(
                    f'institutional_mail_{integrante.id}')
                integrante.user.save()
                integrante.save()
            return redirect('projects')

        except ValueError:
            return render(request, 'projects/project_edit.html', {
                'project': project,
                'integrantes': integrantes,
                'error': 'Error al actualizar los datos'
            })


@login_required
def project_document_edit(request, id_document):
    document = get_object_or_404(Document, pk=id_document)
    if request.method == 'GET':
        return render(request, 'projects/documents/document_edit.html', {
            'document': document
        })

    else:
        project_id = document.project_id

        document.title_doc = request.POST.get("title_doc")
        document.content_doc = request.POST.get("content_doc")
        document.date_uploaded = request.POST.get("date_uploaded")
        document.upload_path = request.POST.get("upload_path")
        document.save()

        return redirect('project_info', id=project_id)


""" Funcion para agregar una retroalimentacion a la tarea del proyecto """


@login_required
def task_feedback(request, id_task):
    task = get_object_or_404(Task, pk=id_task)

    if request.method == "GET":
        return render(request, 'tasks/task_feedback.html', {
            'task': task
        })
    else:
        id_project = task.project_id
        id_activity = task.activity_id

        task.feedback = request.POST.get("feedback")
        task.save()

        return redirect('project_activities_tasks', id_project, id_activity)


@login_required
def task_edit(request, id_task):
        documents = Document.objects.all()
        task = get_object_or_404(Task, pk=id_task)
        if request.method == "GET":
            return render(request, 'tasks/task_edit.html', {
                'task': task,
                'documents': documents
            })
        else:
            task.title = request.POST.get("title")
            task.description = request.POST.get("description")
            new_status = request.POST.get('statusSelect')
            if new_status == 'Completado':
                task.date_completed = timezone.now()
            else:
                task.date_completed = None
            task.status = new_status
            task.document_id = request.POST.get("documentSelect")
            task.important = bool(request.POST.get("important"))

            task.save()
            
            return redirect('project_activities_tasks', task.project_id, task.activity_id)
        

@login_required
def project_detail(request, id):
    project = get_object_or_404(Project, pk=id)
    integrantes = Studentuser.objects.select_related(
        'user').filter(project=project)
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'integrantes': integrantes
    })


@login_required
def project_document_detail(request, id_document):
    document = get_object_or_404(Document, pk=id_document)
    return render(request, 'projects/documents/document_detail.html', {
        'document': document
    })


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/task_detail.html',{'task':task})

@login_required
def complete_task(request, task_id):
    task_id = 1
    print("Funcion para marcar una tarea como completa")


@login_required
def delete_task(request, task_id):
    task_id = 1
    print("Funcion para eliminar tareas")
