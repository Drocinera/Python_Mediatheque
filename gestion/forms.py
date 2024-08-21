from django import forms
from .models import Emprunteur, Livre, DVD, CD, JeuDePlateau


class EmprunteurForm(forms.ModelForm):
    class Meta:
        model = Emprunteur
        fields = ['name']


class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['name', 'auteur', 'disponible']


class DVDForm(forms.ModelForm):
    class Meta:
        model = DVD
        fields = ['name', 'realisateur', 'disponible']


class CDForm(forms.ModelForm):
    class Meta:
        model = CD
        fields = ['name', 'artiste', 'disponible']


class JeuDePlateauForm(forms.ModelForm):
    class Meta:
        model = JeuDePlateau
        fields = ['name', 'createur']
