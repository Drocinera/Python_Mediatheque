from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Emprunteur, Livre, DVD, CD, JeuDePlateau, Emprunt
from django.utils import timezone
from .forms import EmprunteurForm, LivreForm, DVDForm, CDForm, JeuDePlateauForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
import logging


def home_view(request):
    return render(request, 'gestion/home.html')


def is_bibliothecaire(user):
    return user.groups.filter(name='Bibliothécaires').exists()


@login_required
def select_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'bibliothecaire':
            return redirect('gestion:login_bibliothecaire')
        elif role == 'membre':
            return redirect('gestion:membre_home')
    return render(request, 'gestion/select_role.html')


def login_bibliothecaire(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.groups.filter(name='Bibliothécaires').exists():
            login(request, user)
            return redirect('gestion:bibliothecaire_home')
        else:
            return render(request, 'gestion/login_bibliothecaire.html', {'error': 'Identifiants invalides ou non autorisés'})
    return render(request, 'gestion/login_bibliothecaire.html')


@login_required
def changer_role_view(request):
    logout(request)
    return redirect('gestion:select_role')


@login_required
def bibliothecaire_home(request):
    return render(request, 'gestion/bibliothecaire_home.html')


@login_required
def membre_home(request):
    return render(request, 'gestion/membre_home.html')


@login_required
@user_passes_test(is_bibliothecaire)
@csrf_exempt
def add_emprunteur(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        emprunteur = Emprunteur(name=data['name'])
        emprunteur.save()
        return JsonResponse({'message': 'Emprunteur ajouté avec succès'})


@login_required
@user_passes_test(is_bibliothecaire)
@csrf_exempt
def add_media_view(request):
    form = None
    selected_media_type = None

    if request.method == 'POST':
        media_type = request.POST.get('media_type')
        selected_media_type = media_type

        if media_type == 'livre':
            form = LivreForm(request.POST or None)
        elif media_type == 'dvd':
            form = DVDForm(request.POST or None)
        elif media_type == 'cd':
            form = CDForm(request.POST or None)
        elif media_type == 'jeudeplateau':
            form = JeuDePlateauForm(request.POST or None)

        if form and form.is_valid():
            form.save()
            return redirect('gestion:list_medias')
    else:
        form = LivreForm()
        selected_media_type = 'livre'

    return render(request, 'gestion/bibliothecaire/add_media.html', {'form': form, 'selected_media_type': selected_media_type})


@login_required
@user_passes_test(is_bibliothecaire)
def create_emprunt_view(request):
    if request.method == 'POST':
        emprunteur_id = request.POST.get('emprunteur')
        livre_id = request.POST.get('livre')

        emprunteur = get_object_or_404(Emprunteur, id=emprunteur_id)
        livre = get_object_or_404(Livre, id=livre_id)

        if livre.disponible:
            emprunt = Emprunt(emprunteur=emprunteur, livre=livre)
            emprunt.save()

            livre.disponible = False
            livre.save()

            return redirect('gestion:list_medias')
        else:
            return render(request, 'gestion/bibliothecaire/create_emprunt.html', {
                'emprunteurs': Emprunteur.objects.all(),
                'livres': Livre.objects.filter(disponible=True),
                'error': "Le livre sélectionné n'est pas disponible"
            })
    else:
        return render(request, 'gestion/bibliothecaire/create_emprunt.html', {
            'emprunteurs': Emprunteur.objects.all(),
            'livres': Livre.objects.filter(disponible=True)
        })


@login_required
@user_passes_test(is_bibliothecaire)
@csrf_exempt
def return_emprunt(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        emprunt = get_object_or_404(Emprunt, id=data['emprunt_id'])

        if not emprunt.returned:
            emprunt.returned = True
            emprunt.save()
            return JsonResponse({'message': 'Emprunt retourné avec succès'})
        else:
            return JsonResponse({'message': 'Emprunt déjà retourné'}, status=400)


@login_required
@user_passes_test(is_bibliothecaire)
def list_emprunteurs_view(request):
    emprunteurs = Emprunteur.objects.all()
    return render(request, 'gestion/bibliothecaire/liste_membres.html', {'membres': emprunteurs})


@login_required
def list_medias_view(request):
    livres = Livre.objects.all()
    dvds = DVD.objects.all()
    cds = CD.objects.all()
    jeux_de_plateau = JeuDePlateau.objects.all()

    # Create a list to hold media statuses
    media_statuses = []

    for livre in livres:
        status = f"{livre.name} - {livre.auteur} (Emprunté)" if not livre.disponible else f"{livre.name} (Disponible)"
        media_statuses.append(status)

    # Pass this to the template
    return render(request, 'gestion/bibliothecaire/list_medias.html', {
        'livres': media_statuses,  # use media_statuses instead of livres
        'dvds': dvds,
        'cds': cds,
        'jeux_de_plateau': jeux_de_plateau,
    })


@login_required
def add_emprunteur_view(request):
    if request.method == 'POST':
        form = EmprunteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion:liste_membres')
    else:
        form = EmprunteurForm()
    return render(request, 'gestion/bibliothecaire/creer_membre.html', {'form': form})


@login_required
@user_passes_test(is_bibliothecaire)
def update_emprunteur_view(request, id):
    emprunteur = get_object_or_404(Emprunteur, id=id)
    if request.method == 'POST':
        form = EmprunteurForm(request.POST, instance=emprunteur)
        if form.is_valid():
            form.save()
            return redirect('gestion:liste_membres')
    else:
        form = EmprunteurForm(instance=emprunteur)
    return render(request, 'gestion/bibliothecaire/mettre_a_jour_membre.html', {'form': form})


@login_required
@user_passes_test(is_bibliothecaire)
def delete_emprunteur_view(request, id):
    emprunteur = get_object_or_404(Emprunteur, id=id)
    if request.method == 'POST':
        emprunteur.delete()
        return redirect('gestion:liste_membres')
    return render(request, 'gestion/bibliothecaire/supprimer_membre.html', {'emprunteur': emprunteur})


@login_required
def list_medias_membre_view(request):
    medias = []
    for model in [Livre, DVD, CD, JeuDePlateau]:
        medias.extend(list(model.objects.all()))
    return render(request, 'gestion/membre/liste_medias.html', {'medias': medias})


logger = logging.getLogger(__name__)


def my_view(request):
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')

    return render(request, 'my_template.html')
