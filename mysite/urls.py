"""
Configuración de URL para el proyecto mysite.

La lista `urlpatterns` enruta las URL a las vistas. Para más información, consulte:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Ejemplos:
Vistas de función
    1. Agregar una importación: `from my_app import views`
    2. Agregar una URL a `urlpatterns`: `path('', views.home, name='home')
Vistas basadas en clases
    1. Agregar una importación: `from other_app.views import Home`
    2. Agregar una URL a `urlpatterns`: `path('', Home.as_view(), name='home')
Incluir otra URLconf
    1. Importar la función `include()`: `from django.urls import include, path`
    2. Agregar una URL a `urlpatterns`: `path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Project APP",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="david.palacios.forero@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
