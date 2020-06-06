from django.shortcuts import render, get_object_or_404, redirect
from .models import Classe
from .forms import FormSceltaClasse


# View per la pagina per la votazione dei prof
def vota(request, pk):
    classe = get_object_or_404(Classe, pk=pk)
    # TODO: fai i passaggi che ti servono (se ti servono)
    return render(request, 'vota.html', {'classe': classe})


# View per la selezione della classe
def seleziona_classe(request):
    # classi = Classe.objects.all()
    # return render(request, 'seleziona_classe.html', {'classi': classi})

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

