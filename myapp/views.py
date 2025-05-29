
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
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import TaskForm, CreateNewProject
from .models import Project
from .models import Task
from django.utils import timezone

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
                    username=request.POST['username'], password=request.POST['password1'], email=request.POST['email'], first_name=request.POST['firstname'],
                    last_name=request.POST['lastname'])
                user.save()
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
def index(request):
    title = ' !Hola, Bienvenido a la App de Django!'
    usuario = request.user
    nombre_completo = usuario.first_name + ' ' + usuario.last_name
    email = usuario.email
    data_user = {
        'nombre_completo' : nombre_completo,
        'email' : email,
    }
    return render(request, 'index.html', {'title': title, 'data_user' : data_user})

@login_required
def projects(request):
    title = 'Proyectos'
    return render(request, 'projects/projectos.html', {'title' : title})


def about(request):
    return render(request, 'about.html')

# Funtion ...

def projects(request):
    # projects = list(Proyect.objects.values())
    projects = Project.objects.all()
    # return JsonResponse(projects, safe=False)
    return render(request, 'projects/projects.html', {'projects': projects})
# # Funtion ...

@login_required
def tasks(request):
    # task = get_object_or_404(Task, id=id)
    # return HttpResponse('Tarea: %s' % task.title)
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks/tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks/tasks.html', {'tasks': tasks})

@login_required
def create_task(request):
    projects = Project.objects.all()
    if (request.method == 'GET'):
        return render(request, 'tasks/create_task.html', {'projects': projects})
    else:
        try:
            project_instance = get_object_or_404(Project,id=request.POST['project'])
            Task.objects.create(
                    title=request.POST['title'], description=request.POST['description'],project=project_instance, 
                    important=bool(request.POST.get('important')),
                    user=request.user
            )
            #form = TaskForm(request.POST)
            # new_task = form.save(commit=False)
            # new_task.user = request.user
            # new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'tasks/create_task.html',{
                'form' : TaskForm(),
                'projects' : projects,
                'error' : 'Por favor intrduzca datoas validos'
            })
        
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'tasks/task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks/task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Error al actualizar tarea'})
        
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')      

def create_project(request):
    if (request.method == 'GET'):
        return render(request, 'projects/create_project.html', {'form': CreateNewProject()})
    else:
        Project.objects.create(name=request.POST["name"])
        return redirect('projects')
    
def project_detail(request, id):
    projectos = get_object_or_404(Project, id=id)
    tasks = Task.objects.filter(project_id=id)
    return render(request, 'projects/detail.html', {
        'project': projectos,
        'tasks' : tasks
    })

# def create_task(request):
#     if (request.method == 'GET'):
#         return render(request, 'tasks/create_task.html', {'form': CreateNewTask()})
#     else:
#         Task.objects.create(
#             title=request.POST['title'], description=request.POST['description'], project_id=2)
#         return redirect('tasks')