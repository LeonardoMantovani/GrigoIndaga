from django import forms
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


# Form per votare un professore
class FormVotaProfessore(forms.ModelForm):

    # def clean_spiegazione(self):
    #     spiegazione = self.cleaned_data['spiegazione']
    #     if spiegazione < 1 or spiegazione > 10:
    #         raise forms.ValidationError("Inserire un voto da 1 a 10")
    #     return spiegazione

    class Meta:
        model = Votazione
        fields = ('spiegazione', 'preparazione', 'valutazioni', 'metodo', 'rapporto')
