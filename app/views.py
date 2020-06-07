from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Classe, Professore, Votazione
from .forms import FormSceltaClasse, FormVotaProfessore


def fine(request):
    professori = Professore.objects.all()
    return render(request, 'fine.html', {'professori': professori})


# View per la pagina per la votazione dei prof
def vota(request, pk):
    # Salva la classe scelta in una variabile
    classe = get_object_or_404(Classe, pk=pk)
    # crea una lista con i nomi dei professori di quella classe
    nomi_professori = classe.professori.split("-")
    # Crea una lista con i modelli dei Professori della classe
    professori = []
    for prof in Professore.objects.all():
        if nomi_professori.__contains__(prof.nome):
            professori.append(prof)

    # Se è una richiesta di tipo POST significa che è stato premuto il pulsante "INVIA" del form
    if request.method == 'POST':
        # Salva le valutazioni inserite (se valide)
        for prof in professori:
            form = FormVotaProfessore(request.POST, prefix=prof.nome)
            if form.is_valid():
                form.save()
                votazione = Votazione.objects.last()
                votazione.salva_votazione(prof.nome)
                votazione.delete()

        # Carica la pagina finale
        return redirect('fine')

    # Se la richiesta non è POST significa che si sta caricando la pagina per la prima volta
    else:
        # Crea un dizionario del tipo {prof: form_del_prof}
        forms_professori = {}

        # Per ogni prof della classe...
        for prof in professori:
            # # Crea una nuova Votazione con il nome del prof
            # votazione = Votazione()
            # votazione.nome_prof = prof.nome

            # Crea un nuovo form per la votazione appena creata e aggiungilo al dizionario
            form = FormVotaProfessore(prefix=prof.nome)
            forms_professori[prof] = form

    return render(request, 'vota.html', {'classe': classe, 'forms_professori': forms_professori})


# View per la selezione della classe
def seleziona_classe(request):
    # Se è una richiesta di tipo POST significa che è stato premuto il pulsante "VAI A VOTARE" del form
    if request.method == 'POST':
        # Salva il form appena compilato in una variabile
        form = FormSceltaClasse(request.POST)
        # Se il form è valido...
        if form.is_valid():
            # Ottieni la Primary Key della classe inserita nel form
            pk_classe = form.cleaned_data['pk_classe']
            # E carica la pagina per la votazione di quella classe
            return redirect('vota', pk=pk_classe)
    # Se la richiesta non è POST significa che si sta caricando la pagina per la prima volta
    else:
        # Crea un nuovo form per la scelta della classe
        form = FormSceltaClasse()

    # Carica la pagina "seleziona_classe" passando il form salvato nella variabile
    return render(request, 'seleziona_classe.html', {'form': form})

