from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
# from .forms import TaskForm, CreateNewProject
from .models import Project, Task, Studentuser, Meeting, Stage, Activity, Document, Multimedia
from django.utils import timezone
from datetime import datetime
import json
from django.urls import reverse
from django.db.models import Count, Q



# Create your views here.

"""Renderizar la página de inicio."""
def home(request):
    return render(request, 'home.html')

""" Gestionar el registro de usuarios. En GET, mostrar el formulario de registro. 
    En POST, crear un usuario si las contraseñas coinciden."""
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

"""Gestionar el inicio de sesión del usuario. En GET, mostrar el formulario de inicio de sesión. 
    En POST, autenticar e iniciar sesión del usuario."""

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

"""Cerrar la sesión del usuario actual y redirigir a la página de inicio de sesión."""
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

""" Mostrar la página de índice principal para los usuarios conectados, mostrando la información del usuario
    y del panel de los proyectos."""
@login_required
def index(request):
    title = ' !Hola, Bienvenido al Sistema de Gestion de Poryectos de Software!'
    data_user = user_data(request)
    return render(request, 'index.html', {'title': title, 'data_user': data_user})

"""Mostrar la página "Acerca de"."""
def about(request):
    return render(request, 'about.html')

# Funtion ...

"""Mostrar una lista de todos los proyectos."""
@login_required
def projects(request):
    integrantes = Studentuser.objects.select_related('user').all()
    data_user = user_data(request)
    return render(request, 'projects/projects.html', {
        'data_user': data_user,
        'integrantes': integrantes})

"""Gestiona la creación de un nuevo proyecto. En GET, muestra el formulario de creación del proyecto. 
    En POST, crea el proyecto."""
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
    """Crear un nuevo documento para un proyecto existente. En GET, muestra el formulario de creación de documento. En POST, crea el documento y redirige a la página de información del proyecto."""

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
    """
    Asignar un integrante a un proyecto.
    En GET, renderiza la plantilla 'projects/project_members.html' con la lista de integrantes disponibles.
    En POST, asocia el integrante seleccionado con el proyecto cuyo id se proporciona en el parámetro 'project_id'.
    Redirige a la página de proyectos.
    En caso de recibir un método no permitido, devuelve un error 400.
    """
    integrantes = Studentuser.objects.select_related('user').all()
    if request.method == 'GET':
        return render(request, 'projects/project_members.html', {'integrantes': integrantes})
    elif request.method == 'POST':
        integrante_id = request.POST.get('integranteSelect')
        project_id = request.POST.get('project_id')

        if not integrante_id or not project_id:
            #return HttpResponseBadRequest("Faltan datos.")
            return JsonResponse({
                "success":False,
                "error": "Debe selecionar un integrante"
            }, status=400)


        integrante = get_object_or_404(Studentuser, pk=integrante_id)
        integrante.project_id = project_id
        integrante.save()

        return JsonResponse(
            {"success": True, "message": "Integrante asignado correctamente."}
        )
    else:
        return JsonResponse({"success":False,"error": "Metodo no permitido"}, status=400)
    
@login_required
def projects_list_members(requesrt):
    project = get_object_or_404(Project, pk=id)
    integrantes = Studentuser.objects.select_related('user').filter(project=project)

@login_required
def resources_json(request,id_activity):
    resources = Multimedia.objects.filter(activity_id = id_activity)
    data = []
    num_sources = 0
    for resource in resources:
        num_sources += 1
        data.append({
            "Nro": num_sources,
            "Titulo": resource.title_content,
            "Link Contenido": f""" 
                                <a href="{resource.link_content}" target="_blank">
                                <button class="btn btn-link">
                                    <span class="btn-label"><i class="fa fa-link"></i></span>
                                    Link.
                                </button>
                                </a>""",
            "Acciones": f"""
                        <div class="form-button-action">
                            <button type="button" class="btn btn-link btn-info btn-lg" title="Ver"
                            data-target="#ModalDetailResourseMultimedia" data-toggle="modal" onclick="tableDetailResource({resource.id})">
                                <i class="fas fa-eye"></i>
                            </button>
                            <button type="button" title="Editar"
                                class="btn btn-link btn-warning btn-lg "
                                data-original-title="Edit Recurso" data-toggle="modal"
                                data-target="#resourcesActivityModalEdit" onclick="formEditResource({resource.id})">
                                <i class="fa fa-edit"></i>
                            </button>
                            <button type="button" data-toggle="modal"
                                data-target="#addModalProjectMembers" title="Eliminar"
                                class="btn btn-link btn-danger btn-lg"
                                data-original-title="Add Student">
                                <i class="fa fa-times"></i>
                            </button>
                        </div>
                        """
        }) 

    return JsonResponse({"data":data})

@login_required
def activities_json(request):
    activities = Activity.objects.all().order_by("etapa_id","id")
    data = []
    num_activities = 0
    for activity in activities:
        num_activities += 1
        data.append({
            "Nro": num_activities,
            "name": activity.title,
            "stage": activity.etapa.title,
            "actions": f""" 
                <div class="btn-group">
                    <button type="button" class="btn btn-info dropdown-toggle"
                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Action
                    </button>
                    <div class="dropdown-menu">
                        <a class="dropdown-item" href="/activity/{activity.id}/resources/view"> 
                            Agregar Recursos
                        </a>
                        <a class="dropdown-item" href="" data-toggle="modal"
                            data-target="#editActivityModal"
                            onclick="formEditActivity({activity.id})"> Modificar Actividad
                        </a>
                        <a class="dropdown-item" href=""data-toggle="modal"
                            data-target="#deleteActivityModal"
                            onclick="formDeleteActivity({activity.id})">Eliminar Actividad
                        </a>
                    </div>
                </div>
            """
        })
    return JsonResponse({"data": data})


@login_required
def projects_json(request):
    if request.user.is_superuser:
        projects = Project.objects.prefetch_related("integrantes__user").all()
    else:
        projects = Project.objects.prefetch_related("integrantes__user").filter(
            integrantes__user=request.user
        )
    
    data = []
    for project in projects:
        # edit_url = reverse("project_edit", args=[project.id])
        integrantes = "; ".join([
            f"{i.user.first_name} {i.user.last_name}" for i in project.integrantes.all()
        ]) or "Sin integrantes"

        data.append({
            "id": project.id,
            "name": project.name,
            "tema": project.tema_investigacion,
            "horario": project.horario_reunion,
            "integrantes": integrantes,
            "actions": f"""
                <div class="form-button-action">
                    <a href="/projects/{project.id}/info/general" class="btn btn-link btn-primary btn-lg" title="Ver">
                        <i class="fas fa-eye"></i>
                    </a>
                   <button type="button" title="Edit Project"
                        class="btn btn-link btn-primary btn-lg "
                        data-original-title="Edit Project" data-toggle="modal"
                        data-target="#addRowModalEdit"
                        onclick="loadForm({project.id})">
                        <i class="fa fa-edit"></i>
                    </button>
                    <button type="button" data-toggle="modal"
                        data-target="#addModalProjectMembers" title="Add Student"
                        class="btn btn-link btn-primary btn-lg"
                        data-original-title="Add Student" data-id="{ project.id }"
                        data-name="{ project.name }">
                        <i class="fas fa-user-friends"></i>
                    </button>
                </div>
            """
        })

    return JsonResponse({"data": data})


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
    integrantes = Studentuser.objects.select_related('user').filter(project_id=id)
    stages = Stage.objects.all()
    activities = Activity.objects.all().order_by("etapa_id","id")
    documents = Document.objects.filter(project_id=id)
    tasks = Task.objects.filter(project_id=id)
    
    # estadisticas tareas y recuentro de las tareas pendintes, en proceso y completadas
    stats_task = tasks.aggregate(
        absolutely=Count("id"),
        earring=Count("id", filter=Q(status="Pendiente")),
        in_progresss = Count("id", filter=Q(status="En proceso")),
        completed=Count("id", filter=Q(status="Completado")),
    )

    task_complete = stats_task["completed"]
    progr_general = 0
    if stats_task["absolutely"] > 0:
        progr_general = (task_complete * 100) / stats_task["absolutely"]

    # ---Estadisticas por estapa ---
    etapas_stats = []
    for stage in stages:
        stage_activities = activities.filter(etapa_id=stage.id)
        stage_task = tasks.filter(activity_id__in=stage_activities)

        stage_stats = stage_task.aggregate(
            total_task = Count("id"),
            pendientes_task = Count("id", filter=Q(status="Pendiente")),
            completado_task = Count("id", filter=Q(status="Completado"))
        )
        total = stage_stats['total_task']
        progress_stage = (stage_stats["completado_task"]*100)/total if total > 0 else 0

        etapas_stats.append({
            "stage": stage,
            "stats": stage_stats,
            "progress_stage": round(progress_stage)
        })
    
    return render(request, 'projects/project_info.html',
                  {
                      'project': project,
                      'integrantes': integrantes,
                      'stages': stages,
                      'activities': activities,
                      'documents': documents,
                      'progr_general': round(progr_general),
                      'tasks': tasks,
                      'stats_task': stats_task,
                      'etapas_stats':etapas_stats
                  })

@login_required
def content_approach_project(request):
    stage = Stage.objects.get(id=1)
    activities = Activity.objects.filter(etapa_id=1).order_by("id")
    return render(request, 'content/content_guide.html',{
        'activities':activities,
        'stage': stage
    })

@login_required
def content_planning_project(request):
    stage = Stage.objects.get(id=2)
    activities = Activity.objects.filter(etapa_id=2).order_by("id")
    return render(request, 'content/content_guide.html',{
        'activities':activities,
        'stage': stage
    })

def content_systemic_review(request):
    stage = Stage.objects.get(id=3)
    activities = Activity.objects.filter(etapa_id=3).order_by("id")
    return render(request, 'content/content_guide.html',{
        'activities':activities,
        'stage': stage
    })

def content_validation(request):
    stage = Stage.objects.get(id=4)
    activities = Activity.objects.filter(etapa_id=4).order_by("id")
    return render(request, 'content/content_guide.html',{
        'activities':activities,
        'stage': stage
    })
def content_subtantiation(request):
    stage = Stage.objects.get(id=5)
    activities = Activity.objects.filter(etapa_id=5).order_by("id")
    return render(request, 'content/content_guide.html',{
        'activities':activities,
        'stage': stage
    })

def content_guide_detail(request,id_activity):
    activity = get_object_or_404(Activity,pk=id_activity)
    resources_multimedia = Multimedia.objects.filter(activity_id=id_activity)
    return render(request, 'content/content_guide_detail.html',{
        'activity':activity,
        'resources_multimedia':resources_multimedia
    })




@login_required
def activities(request):
    stages = Stage.objects.all()
    activities = Activity.objects.all().order_by("etapa_id","id")
    return render(request, 'tasks/activities/activities.html',{
        'stages':stages,
        'activities':activities
    })

@login_required
def activities_list(request):
    activities = Activity.objects.all()
    return render(request, 'tasks/activities/activities_list.html', {
        'activities':activities
    })

@login_required
def activity_create(request):
    if request.method == "GET":
        return render(request, 'tasks/activities/activity_create.html')
    else:
        Activity.objects.create(
            title=request.POST.get("title"),
            description = request.POST.get("description"),
            etapa_id=request.POST.get("stageSelect", ""),

        )
        
        return redirect('activities')
    
@login_required
def activity_edit(request,id_activity):
    activity = get_object_or_404(Activity,pk=id_activity)
    stages = Stage.objects.all()
    if request.method == "GET":
        return render(request, 'tasks/activities/activity_edit.html',
        {
            'stages': stages,
            'activity': activity
        })
    elif request.method == "POST":
            activity.title=request.POST.get("title")
            activity.description = request.POST.get("description")
            activity.etapa_id=request.POST.get("stageSelect") 
            activity.save()

            return JsonResponse(
                {"success": True, "message": "Actividada editada correctamente."}
            )
    else:
        return JsonResponse({"success":False,"error": "Metodo no permitido"}, status=400)
       
@login_required
def activity_delete(request,id_activity):
    activity = get_object_or_404(Activity,pk=id_activity)
    if request.method == 'GET':
         return render(request,'tasks/activities/activity_delete.html',{
            'activity': activity
        })
    else:
        activity.delete()
        return redirect('activities')
       

@login_required
def project_activities_tasks(request, id, id_activity):
    project = get_object_or_404(Project, pk=id)
    activity = get_object_or_404(Activity, pk=id_activity)
    tasks = Task.objects.filter(activity_id=id_activity, project_id=id)
    documents = Document.objects.filter(project_id=id)
    if request.method == 'GET':
        return render(request, 'tasks/activities/activities_tasks_view.html', {
            'project': project,
            'activity': activity,
            'tasks': tasks,
            'documents': documents
        })

@login_required
def activity_resources(request, id_activity):
    activity = get_object_or_404(Activity, pk=id_activity)
    resources = Multimedia.objects.filter(activity_id=id_activity)
    return render(request, 'tasks/activities/resources/activity_resources.html', {
        'activity': activity,
        'resources': resources
    })

@login_required
def activity_resources_add(request):
    if request.method == 'GET':
        return render(request, 'tasks/activities/resources/resource_add.html')
    elif request.method == 'POST':
        if not request.POST.get("title_content"):
            return JsonResponse(
                {"success": False, "error": "El título es obligatorio."}
            )
        else:
            Multimedia.objects.create(
                title_content=request.POST.get("title_content"),
                description=request.POST.get("description"),
                link_content=request.POST.get("link_content"),
                activity_id=request.POST.get("id_activity")
            )

        return JsonResponse(
            {"success": True, "message": "Recursos multimedia agregados correctamente."}
        )
        
@login_required
def activity_resources_edit(request,id_resource):
    resource_multimedia = get_object_or_404(Multimedia,pk=id_resource)
    if request.method == "GET":
        return render(request,'tasks/activities/resources/resource_edit.html',{
            'resource':resource_multimedia
        })
    elif request.method == "POST":
        resource_multimedia.title_content = request.POST.get("title_content")
        resource_multimedia.description = request.POST.get("description")
        resource_multimedia.link_content = request.POST.get("link_content")
        resource_multimedia.save()

        return JsonResponse(
            {"success": True, "message": "Recursos multimedia modificado correctamente."}
        )
    
@login_required
def activity_resources_detail(request,id_resource):
    resource_multimedia = get_object_or_404(Multimedia,pk=id_resource)
    return render(request,'tasks/activities/resources/resource_detail.html',{
            'resource':resource_multimedia
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

""" Gestionar la creación de una nueva tarea. En GET, mostrar el formulario de creación de tareas. 
    En POST, crear la tarea."""
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
    integrantes = Studentuser.objects.select_related('user').filter(project=project)

    if request.method == 'POST':
            # Actualizar proyecto
            project.name = request.POST.get('name')
            project.horario_reunion = request.POST.get('horario_reunion')
            project.tema_investigacion = request.POST.get('tema_investigacion')
            project.save()

            # Actualizar integrantes
            for integrante in integrantes:
                integrante.user.first_name = request.POST.get(f'integrante_first_name_{integrante.id}')
                integrante.user.last_name = request.POST.get(f'integrante_last_name_{integrante.id}')
                integrante.cedula = request.POST.get(f'cedula_{integrante.id}')
                integrante.student_code = request.POST.get(f'student_code_{integrante.id}')
                integrante.user.email = request.POST.get(f'institutional_mail_{integrante.id}')
                integrante.user.save()
                integrante.save()
            return redirect('projects')
    elif request.method == 'GET':
         return render(request, 'projects/project_edit.html', {
            'project': project,
            'integrantes': integrantes
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


""" 
Funcion para agregar una retroalimentacion a la tarea del proyecto
"""
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
        
"""
 Muestra los detalles y las tareas asociadas a un proyecto específico.
"""
@login_required
def project_detail(request, id):
    project = get_object_or_404(Project, pk=id)
    integrantes = Studentuser.objects.select_related('user').filter(project=project)
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

"""Mostrar y actualizar los detalles de una tarea específica perteneciente al usuario conectado."""
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

@login_required
def calendar(request):
    fecha_hora_actual = datetime.now()
    fecha_actual = fecha_hora_actual.strftime('%Y-%m-%d')
    projects = Project.objects.all().order_by('id')
    return render(request, 'mappings/calendar.html',{
        'fecha_actual': fecha_actual,
        'projects': projects
        
    })

@login_required
def calendar_create_event(request):
    
    if request.method == 'GET':
        return render(request,'mappings/calendar_create_event.html')
    elif request.method == 'POST':
        if not request.POST.get("title") or not request.POST.get('projectSelect') or not request.POST.get('meeting_start') or not request.POST.get('meeting_end'):
            return JsonResponse(
                {"success": False, "error": "Llenar los campos obligarios"}
            )

        Meeting.objects.create(
            title = request.POST.get('title'),
            agenda = request.POST.get('agenda'),
            project_id = request.POST.get('projectSelect'),
            meeting_start = request.POST.get('meeting_start'),
            meeting_end = request.POST.get('meeting_end'),
            meeting_link = request.POST.get('meeting_link')
        )
        return JsonResponse({ "status": "success", "message": "Evento creado correctamente."})
    else:
        return JsonResponse({"status":"error", "message": "Metodo no permitido"}, status=405)

@login_required
def calendar_event_detatils(request, id_meeting):
    meeting = get_object_or_404(Meeting, pk=id_meeting)
    projects = Project.objects.all().order_by('id')

    project_id = meeting.project_id
    integrantes = Studentuser.objects.select_related('user').filter(project=project_id)

    return render(request, 'mappings/calendar_event_detail.html',{
        'meeting': meeting,
        'projects': projects,
        'integrantes': integrantes
    })

@login_required
def calendar_create_note(request, id_meeting):
    meeting = get_object_or_404(Meeting, pk=id_meeting)

    if request.method == 'POST':
        meeting_note = request.POST.get('notes')
        
        meeting.notes = meeting_note
        meeting.save()

        return JsonResponse({ "status": "success", "message": "Nota creada correctamente."})
    
    else:     
        return render(request, 'mappings/calendar_create_note.html',{
            'meeting': meeting
        })

def calendar_event_info(request, id_meeting):
    meeting = get_object_or_404(Meeting, pk=id_meeting)
   
    return render(request, 'mappings/calendar_event_info.html',{
        'meeting': meeting
    })

def calendar_event_edit(request, id_meeting):
    meeting = get_object_or_404(Meeting, pk=id_meeting)

    if request.method == 'POST':
        try:
            meeting.title = request.POST.get('title')
            meeting.agenda = request.POST.get('agenda')
            meeting.project_id = request.POST.get('projectSelect')
            meeting.meeting_start = request.POST.get('meeting_start')
            meeting.meeting_end = request.POST.get('meeting_end')
            meeting.meeting_link = request.POST.get('meeting_link')
            meeting.save()

            return JsonResponse({ "status": "success", "message": "Evento editado correctamente."})
        except Exception as e:
            return JsonResponse({ 'status': 'error', 'message': str(e)},status=400)
    
    else:     
        return render(request, 'mappings/calendar_event_edit.html',{
            'meeting': meeting
        })

@login_required
def calendar_event_delete(request, id_meeting):
    meeting = get_object_or_404(Meeting, pk=id_meeting)
    meeting.delete()
    return JsonResponse({ "status": "success", "message": "Evento eliminado correctamente."})

def calendar_event_json(request):
    Meetings = Meeting.objects.all()

    events = []

    for meeting in Meetings:
        events.append({
            'title': meeting.project.name,
            'start': meeting.meeting_start.isoformat(),
            'end': meeting.meeting_end.isoformat(),
            'url': f"/calendar/{meeting.id}/event/detail",
        })

    return JsonResponse(events, safe=False)