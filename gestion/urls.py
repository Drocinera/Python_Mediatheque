from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('', views.select_role, name='select_role'),
    path('bibliothecaire/', views.login_bibliothecaire, name='login_bibliothecaire'),
    path('changer-role/', views.changer_role_view, name='changer_role'),
    path('bibliothecaire/home', views.bibliothecaire_home, name='bibliothecaire_home'),
    path('membre/', views.membre_home, name='membre_home'),
    path('membres/', views.list_emprunteurs_view, name='liste_membres'),
    path('membre/creer/', views.add_emprunteur_view, name='creer_membre'),
    path('membre/<int:id>/modifier/', views.update_emprunteur_view, name='mettre_a_jour_membre'),
    path('membres/<int:id>/supprimer/', views.delete_emprunteur_view, name='supprimer_membre'),
    path('medias/', views.list_medias_view, name='list_medias'),
    path('media/creer/', views.add_media_view, name='add_media'),
    path('emprunt/creer/', views.create_emprunt_view, name='create_emprunt'),
    path('medias/membre/', views.list_medias_membre_view, name='liste_medias_membre'),
]
