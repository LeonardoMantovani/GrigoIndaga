from django.db import models
from django.shortcuts import get_object_or_404

# Evita di controllare views.py prima di eseguire le migrations (altrimenti queste non andrebbero a buon fine)
from django.core.management.base import BaseCommand
BaseCommand.requires_system_checks = False


# Modello Classe
class Classe(models.Model):
    # Nome della classe (es: 1A sci)
    nome = models.CharField(max_length=6)
    # Cognomi e Nomi dei professori, separati da 1 virgola
    professori = models.TextField()

    # identifica il modello con il nome della classe (per riconoscere i modelli nella sezione admin)
    def __str__(self):
        return self.nome


# Modello Materia
class Materia(models.Model):
    # Nome della materia (es: Disegno e Storia dell'Arte)
    nome = models.CharField(max_length=100)

    # Identifica il modello con il nome della materia
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
    # Numero di voti ricevuti
    n_voti = models.IntegerField(default=0)

    # Proprietà per accedere alle medie dei punteggi
    @property
    def media_spiegazione(self):
        if self.n_voti <= 0:
            return 0
        else:
            return round(self.spiegazione / self.n_voti, 1)

    @property
    def media_preparazione(self):
        if self.n_voti <= 0:
            return 0
        else:
            return round(self.preparazione / self.n_voti, 1)

    @property
    def media_valutazioni(self):
        if self.n_voti <= 0:
            return 0
        else:
            return round(self.valutazioni / self.n_voti, 1)

    @property
    def media_metodo(self):
        if self.n_voti <= 0:
            return 0
        else:
            return round(self.metodo / self.n_voti, 1)

    @property
    def media_rapporto(self):
        if self.n_voti <= 0:
            return 0
        else:
            return round(self.rapporto / self.n_voti, 1)

    @property
    def punteggio_totale(self):
        return (self.media_spiegazione + self.media_preparazione + self.media_valutazioni + self.media_metodo + self.media_rapporto) / 5

    # Metodo per aumentare i punteggi in seguito ad una nuova votazione
    def aumenta_punteggi(self, spiegazione, preparazione, valutazioni, metodo, rapporto):
        self.spiegazione += spiegazione
        self.preparazione += preparazione
        self.valutazioni += valutazioni
        self.metodo += metodo
        self.rapporto += rapporto
        self.n_voti += 1
        self.save()

    # identifica il modello con il nome del professore (per riconoscere i modelli nella sezione admin)
    def __str__(self):
        return self.nome

    # modifica il metodo per salvare il professore affinché aggiunga la sua materia se non è presente nel database
    # def save(self, *args, **kwargs):
    #     if not Materia.objects.filter(nome=self.materia).exists():
    #         nuova_materia = Materia(nome=self.materia)
    #         nuova_materia.save()
    #
    #     super().save(self, *args, **kwargs)
    # (RIMOSSO PERCHè PROVOCAVA UN ERRORE)



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
