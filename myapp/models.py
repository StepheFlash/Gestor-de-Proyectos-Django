from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=200)
    tema_investigacion = models.TextField(max_length=200, blank=True)
    horario_reunion = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Studentuser(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True, related_name='integrantes')
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=20, blank=True)
    student_code = models.CharField(max_length=20,blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()}({self.cedula})"
    
class Meeting(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,blank=True)
    meeting_start = models.DateTimeField()
    meeting_end = models.DateTimeField()
    agenda = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    meeting_link = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.title} (Proyecto: {self.project.name})"

class Document(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    title_doc = models.CharField(max_length=150)
    content_doc = models.TextField(blank=True)
    upload_path = models.URLField(blank=True)
    feedback = models.TextField(blank=True)
    date_uploaded = models.DateField(null=True)
    

    def __str__(self):
        return f"{self.title_doc} (Proyecto: {self.project.name})"

#Tabla estapas(plantilla)
class Stage(models.Model):
    title = models.CharField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

#Tabla actividades(plantilla)
class Activity(models.Model):
    etapa = models.ForeignKey(Stage, on_delete=models.CASCADE)
    title = models.CharField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} (Etapa: {self.etapa.title})"


class Task(models.Model):
    # on_delete=models.CASCADE es una funcion que se encarga de borrar los datos relacionados
    #Llaves foraneas
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, blank=True, null=True)
    activity = models.ForeignKey(Activity,on_delete=models.CASCADE) 
    #user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    #Datos propios de la tabla
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(default = 'Pendiente')
    date_created = models.DateTimeField(default=timezone.now)
    date_completed = models.DateTimeField(null=True,blank=True)
    feedback = models.TextField(blank=True)
    important = models.BooleanField(default=False)

    # //Funcion para cambiar el titulo de las listas desde el admin
    def __str__(self):
        return f"{self.title} (Proyecto: {self.project.name})"


class Multimedia(models.Model):
    title_content = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    link_content = models.URLField(blank=True)
    activity = models.ForeignKey(Activity,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title_content} (Actividad: {self.activity.title})"

