"""
URL configuration for tecsus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# from alerta.views import AlertaAguaAPIView
# from .view import UploadCSVView, EnviarEmailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/energia/', include('energia.urls')), 
    path('api/v1/', include('djoser.urls.jwt')),
    path('api/agua/', include('agua.urls')), 
    path('api/alerta/', include('alerta.urls')),
    path('api/v1/user/', include('user_management.urls')),
    # path('enviar-email/<str:email>/', EnviarEmailView.as_view(), name='enviar_email'),
]
