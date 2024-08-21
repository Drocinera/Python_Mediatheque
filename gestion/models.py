from django.db import models
from django.utils import timezone


class Emprunteur(models.Model):
    name = models.CharField(max_length=255)
    bloque = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Livre(models.Model):
    name = models.CharField(max_length=255)
    auteur = models.CharField(max_length=255)
    date_emprunt = models.DateField(null=True, blank=True)
    disponible = models.BooleanField(default=True)
    emprunteur = models.ForeignKey(Emprunteur, null=True, blank=True, on_delete=models.SET_NULL, related_name='livres_empruntes')


class DVD(models.Model):
    name = models.CharField(max_length=255)
    realisateur = models.CharField(max_length=255)
    date_emprunt = models.DateField(null=True, blank=True)
    disponible = models.BooleanField(default=True)
    emprunteur = models.ForeignKey(Emprunteur, null=True, blank=True, on_delete=models.SET_NULL, related_name='dvds_empruntes')


class CD(models.Model):
    name = models.CharField(max_length=255)
    artiste = models.CharField(max_length=255)
    date_emprunt = models.DateField(null=True, blank=True)
    disponible = models.BooleanField(default=True)
    emprunteur = models.ForeignKey(Emprunteur, null=True, blank=True, on_delete=models.SET_NULL, related_name='cds_empruntes')


class JeuDePlateau(models.Model):
    name = models.CharField(max_length=255)
    createur = models.CharField(max_length=255)


class Emprunt(models.Model):
    emprunteur = models.ForeignKey(Emprunteur, on_delete=models.CASCADE)  # Corrigé ici
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, null=True, blank=True)
    cd = models.ForeignKey(CD, on_delete=models.CASCADE, null=True, blank=True)
    dvd = models.ForeignKey(DVD, on_delete=models.CASCADE, null=True, blank=True)
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.date_retour and self.date_retour < timezone.now():
            if self.livre:
                self.livre.disponible = True
                self.livre.save()
            if self.dvd:
                self.dvd.disponible = True
                self.dvd.save()
            if self.cd:
                self.cd.disponible = True
                self.cd.save()
            self.emprunteur.bloque = True
            self.emprunteur.save()
