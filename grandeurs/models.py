from django.db import models

class Grandeur(models.Model):
    nom = models.CharField(max_length= 60)
    unite = models.CharField(max_length= 30)
    # valeur_min de type Float
    valeur_min = models.FloatField()
    # valeur_max de type Float
    valeur_max = models.FloatField()

    def __str__(self):
        return f'{self.nom} Unité: {self.unite} valeurs entre {self.valeur_min} et {self.valeur_max}'

class Mesure(models.Model):
    valeur = models.FloatField()
    date_prise = models.DateTimeField()
    grandeur = models.ForeignKey('Grandeur', on_delete = models.CASCADE)

    def __str__(self):
        return f'Mesure: {self.valeur} at {self.date_prise}'