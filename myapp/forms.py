# from cProfile import label
# from ftplib import MAXLINE
from django.forms import ModelForm
from django import forms
from .models import Task, Project

# class CreateNewTask(forms.Form):
#     title = forms.CharField(label="Titulo de tarea", max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))
#     description = forms.CharField(label="Descripcion de la tarea", widget=forms.Textarea(attrs={'class' : 'input'}))
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task 
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Escribe titulo de la tarea'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder' : 'Escribe descripcion de la tarea' }),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }
    
class CreateNewProject(forms.Form):
    name = forms.CharField(label="Nombre del proyecto", max_length=200)
    horario_reunion = forms.CharField(label="Horario de reunion", max_length=400)
    tema_investigacion = forms.CharField(label="Tema de investigacion", max_length=400)
