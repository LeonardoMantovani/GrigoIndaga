from django.db import models


# Modello Classe
class Classe(models.Model):
    # Nome della classe (es: 1A sci)
    nome = models.CharField(max_length=6)
    # Cognomi e Nomi dei professori, separati da 1 virgola
    professori = models.TextField()

    # identifica il modello con il nome della classe (per riconoscere i modelli nella sezione admin)
    def __str__(self):
        return self.nome
