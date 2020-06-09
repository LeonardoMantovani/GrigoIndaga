from django import forms
from django.utils.safestring import mark_safe
from .models import Classe, Votazione


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

        # Crea una lista per le "choices" dei widgets RadioSelect composta 10 stelle
        StelleDa1a10 = [
            (1, mark_safe('<i class="fa fa-star" aria-hidden="true"></i>')),
            (2, mark_safe('<i class="fa fa-star" aria-hidden="true"></i>')),
            (3, mark_safe('<i class="fa fa-star" aria-hidden="true"></i>')),
            (4, mark_safe('<i class="fa fa-star" aria-hidden="true"></i>')),
            (5, mark_safe('<i class="fa fa-star" aria-hidden="true"></i>')),
            (6, mark_safe('<i class="fa fa-star" aria-hidden="true"></i>')),
            (7, mark_safe('<i class="fa fa-star" aria-hidden="true"></i>')),
            (8, mark_safe('<i class="fa fa-star" aria-hidden="true"></i>')),
            (9, mark_safe('<i class="fa fa-star" aria-hidden="true"></i>')),
            (10, mark_safe('<i class="fa fa-star" aria-hidden="true"></i>'))
        ]

        # Imposta il widget di ogni parametro come un RadioSelect di 10 stelle
        widgets = {
            'spiegazione': forms.RadioSelect(choices=StelleDa1a10),
            'preparazione': forms.RadioSelect(choices=StelleDa1a10),
            'valutazioni': forms.RadioSelect(choices=StelleDa1a10),
            'metodo': forms.RadioSelect(choices=StelleDa1a10),
            'rapporto': forms.RadioSelect(choices=StelleDa1a10),
        }
