from django.contrib import admin
from django.urls import path, include
from gestion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gestion/', include('gestion.urls')),
    path('', views.select_role, name='select_role'),  # URL pour la page d'accueil
]
