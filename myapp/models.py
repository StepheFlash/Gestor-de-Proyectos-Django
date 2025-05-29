from django.db import models
"""
Este módulo define los modelos de datos de la aplicación.
Clases:
    Proyecto: Representa un proyecto con un nombre.
    Tarea: Representa una tarea asociada a un proyecto y un usuario, incluyendo detalles como título, descripción, fecha de creación, fecha de finalización e importancia.
Modelos:
  Proyecto:
    Campos:
        name (CharField): El nombre del proyecto.
    Métodos:
        __str__: Devuelve el nombre del proyecto.
  Tarea:
    Campos:
        title (CharField): El título de la tarea.
        description (TextField): La descripción de la tarea (opcional).
        roject (ForeignKey): Referencia al proyecto asociado.
        created (DateTimeField): Marca de tiempo de creación de la tarea.
        datecompleted (DateTimeField): Marca de tiempo de finalización de la tarea (opcional).
        important (BooleanField): Indica si la tarea es importante. usuario (ForeignKey): Referencia al usuario propietario de la tarea.
    Métodos:
    __str__: Devuelve una cadena que representa la tarea, incluyendo su título y el nombre de usuario del propietario.
"""
from django.contrib.auth.models import User

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=200)
    #description = models.TextField(max_length=500,blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # on_delete=models.CASCADE es una funcion que se encarga de borrar los datos relacionados
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    #done = models.BooleanField(default=False)

    #Campo nuevos
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #//Funcion para cambiar el titulo de las listas desde el admin
    def __str__(self):
        return self.title + ' de ' + self.user.username
    