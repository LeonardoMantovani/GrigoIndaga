from django.core.management.base import BaseCommand
from app.models import Studente, Professore


class Command(BaseCommand):
    help = 'Azzera tutti i punteggi dei professori e restituisce la possibilità di votare a tutti gli studenti'

    def handle(self, *args, **options):
        for studente in Studente.objects.all():
            studente.ha_votato = False
            studente.save()

        for prof in Professore.objects.all():
            prof.spiegazione = 0
            prof.preparazione = 0
            prof.valutazioni = 0
            prof.metodo = 0
            prof.rapporto = 0
            prof.n_voti = 0
            prof.save()

        self.stdout.write('Reset mensile effettuato con successo')