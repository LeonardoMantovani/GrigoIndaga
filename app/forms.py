from django import forms
from django.utils.safestring import mark_safe
from .models import Classe, Votazione, Materia


# Form per la scelta della classe
class FormSceltaClasse(forms.Form):
    # Salva i modelli Classe in una lista
    classi = Classe.objects.all()
    # Crea una lista vuota per il dropdown
    lista_classi = []
    # Per ogni modello Classe nella lista...
    for classe in classi:
        # Aggiungi alla lista per il dropdown la Primary Key della classe (per identificarla nel codice)
        # e il suo nome (per renderla identificabile dall'utente)
        lista_classi += [(classe.pk, classe.nome)]

    # Crea un campo del form nome_classe per l'input dell'utente
    pk_classe = forms.CharField(label="In che classe sei?", widget=forms.Select(choices=lista_classi))


class ReadOnlyText(forms.TextInput):
    input_type = 'text'

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        return value


# Form per votare un professore
class FormVotaProfessore(forms.ModelForm):

    class Meta:
        model = Votazione
        fields = ('spiegazione', 'preparazione', 'valutazioni', 'metodo', 'rapporto')
        labels = {
            'spiegazione': 'Chiarezza nelle Spiegazioni',
            'preparazione': 'Preparazione',
            'valutazioni': 'Adeguatezza delle Valutazioni',
            'metodo': 'Efficacia del metodo',
            'rapporto': 'Rapporto con gli Studenti',
        }

        # Crea una lista per le "choices" dei widgets RadioSelect composta dai numeri da 1 a 10
        StelleDa1a10 = [
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
            (6, '6'),
            (7, '7'),
            (8, '8'),
            (9, '9'),
            (10, '10')
        ]

        # Imposta il widget di ogni parametro come un RadioSelect di 10 stelle
        widgets = {
            'spiegazione': forms.RadioSelect(choices=StelleDa1a10),
            'preparazione': forms.RadioSelect(choices=StelleDa1a10),
            'valutazioni': forms.RadioSelect(choices=StelleDa1a10),
            'metodo': forms.RadioSelect(choices=StelleDa1a10),
            'rapporto': forms.RadioSelect(choices=StelleDa1a10),
        }


# Form per filtrare la classifica (per materia insegnata)
class FormFiltraClassifica(forms.Form):
    # Salva i modelli Classe in una lista
    materie = Materia.objects.all()
    # Crea una lista vuota per il dropdown
    lista_materie = []
    # Per ogni modello Classe nella lista...
    for materia in materie:
        # Aggiungi alla lista per il dropdown la Primary Key della classe (per identificarla nel codice)
        # e il suo nome (per renderla identificabile dall'utente)
        lista_materie += [(materia.pk, materia.nome)]

    # Crea un campo del form nome_classe per l'input dell'utente
    pk_materia = forms.CharField(label='Materia', widget=forms.Select(choices=lista_materie))
