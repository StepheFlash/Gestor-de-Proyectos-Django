from django.contrib import admin

from .models import Project,Stage,Activity,Document,Task, Studentuser, Multimedia, Meeting


# Register your models here.
#Clase para mostrar los el campo de fecha de creacion en el panel del admin
class TaskProjectAdmin(admin.ModelAdmin):
    readonly_fields = ("date_created",)
#Importa los modelos al panel del administrador 
admin.site.register(Project)
admin.site.register(Studentuser)
admin.site.register(Task, TaskProjectAdmin)
admin.site.register(Stage)
admin.site.register(Activity)
admin.site.register(Document)
admin.site.register(Multimedia)
admin.site.register(Meeting)



