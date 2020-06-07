from django.db import models
from django.shortcuts import get_object_or_404


# Modello Classe
class Classe(models.Model):
    # Nome della classe (es: 1A sci)
    nome = models.CharField(max_length=6)
    # Cognomi e Nomi dei professori, separati da 1 virgola
    professori = models.TextField()

    # identifica il modello con il nome della classe (per riconoscere i modelli nella sezione admin)
    def __str__(self):
        return self.nome


# Modello Professore
class Professore(models.Model):
    # Nome del professore (es: Rosso Andrea)
    nome = models.CharField(max_length=50)
    # Materia insegnata dal professore TODO: lasciare CharField o trasformare in enumerazione?
    materia = models.CharField(max_length=20)
    # Punteggi (somma dei voti per ogni parametro)
    spiegazione = models.IntegerField(default=0)
    preparazione = models.IntegerField(default=0)
    valutazioni = models.IntegerField(default=0)
    metodo = models.IntegerField(default=0)
    rapporto = models.IntegerField(default=0)

    # Metodo per aumentare i punteggi in seguito ad una nuova votazione
    def aumenta_punteggi(self, spiegazione, preparazione, valutazioni, metodo, rapporto):
        self.spiegazione += spiegazione
        self.preparazione += preparazione
        self.valutazioni += valutazioni
        self.metodo += metodo
        self.rapporto += rapporto
        self.save()

    # identifica il modello con il nome del professore (per riconoscere i modelli nella sezione admin)
    def __str__(self):
        return self.nome


class Votazione(models.Model):
    # Voti
    spiegazione = models.IntegerField()
    preparazione = models.IntegerField()
    valutazioni = models.IntegerField()
    metodo = models.IntegerField()
    rapporto = models.IntegerField()

    # Metodo per salvare la votazione
    def salva_votazione(self, nome_prof):
        prof = get_object_or_404(Professore, nome=nome_prof)
        prof.aumenta_punteggi(self.spiegazione, self.preparazione, self.valutazioni, self.metodo, self.rapporto)
