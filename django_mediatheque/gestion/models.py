from django.db import models
from django.utils import timezone
from datetime import timedelta


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
    emprunteur = models.ForeignKey(Emprunteur, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, null=True, blank=True, on_delete=models.CASCADE)
    dvd = models.ForeignKey(DVD, null=True, blank=True, on_delete=models.CASCADE)
    cd = models.ForeignKey(CD, null=True, blank=True, on_delete=models.CASCADE)
    date_emprunt = models.DateField(default=timezone.now)
    date_retour = models.DateField(default=timezone.now() + timedelta(days=7))
    returned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.returned:
            if self.livre:
                self.livre.disponible = True
                self.livre.save()
            if self.dvd:
                self.dvd.disponible = True
                self.dvd.save()
            if self.cd:
                self.cd.disponible = True
                self.cd.save()

        if not self.returned and self.date_retour < timezone.now():
            self.emprunteur.bloque = True
            self.emprunteur.save()
