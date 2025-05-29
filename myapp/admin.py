from django.contrib import admin

from .models import Project, Task


# Register your models here.
#Clase para mostrar los el campo de fecha de creacion en el panel del admin
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)
#Importa los modelos al panel del administrador 
admin.site.register(Project)
admin.site.register(Task, TaskAdmin)


