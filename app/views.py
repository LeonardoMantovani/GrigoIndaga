from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Classe, Professore, Votazione, Materia, Studente
from .forms import FormSceltaClasse, FormVotaProfessore, FormFiltraClassifica
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required


def fine(request):
    professori = Professore.objects.all()
    return render(request, 'fine.html', {'professori': professori})


# View per la pagina per la votazione dei prof
def vota(request, pk):
    # Se l'utente ha fatto il login...
    if request.user.is_authenticated:
        # Controlla che non abbia già votato e poi...
        if request.user.studente.ha_votato:
            return HttpResponse('<h2>Hai già votato questo mese</h2>')
        else:
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

                # Segna che l'utente ha votato
                studente = get_object_or_404(Studente, user=request.user)
                studente.ha_votato = True
                studente.save()

                # Carica la pagina finale
                return redirect('fine')

            # Se la richiesta non è POST significa che si sta caricando la pagina per la prima volta
            else:
                # Crea un dizionario del tipo {prof: form_del_prof}
                forms_professori = {}

                # Per ogni prof della classe...
                for prof in professori:
                    # Crea un nuovo form per la votazione appena creata e aggiungilo al dizionario
                    form = FormVotaProfessore(prefix=prof.nome)
                    forms_professori[prof] = form

            return render(request, 'vota.html', {'classe': classe, 'forms_professori': forms_professori})
    else:
        # Altrimenti carica la pagina di Accesso Negato
        return render(request, 'no_login.html', {})


# View per la selezione della classe
def seleziona_classe(request):
    # Crea (se neccessario) un modello Studente corrispondente all'utente loggato
    if request.user.is_authenticated:
        # Crea una variabile per verificare l'esistenza dell'utente tra gli Studenti
        esiste_studente = False

        # Controlla se l'utente è presente tra gli studenti
        for studente in Studente.objects.all():
            if studente.user == request.user:
                esiste_studente = True

        # Se dopo il controllo non è stato trovato uno studente corrispondente all'utente creane uno nuovo
        if esiste_studente == False:
            nuovo_studente = Studente(user=request.user)
            nuovo_studente.save()

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
    return render(request, 'index.html', {'form': form})


def ottieni_punteggio(professore):
    return professore.punteggio_totale


# View per vedere i risultati
def risultati(request):
    context = {}

    # Se l'utente ha fatto il login...
    if request.user.is_authenticated:
        # Crea una lista dei professori che sono stati votati
        professori_votati = []
        for prof in Professore.objects.all():
            if prof.n_voti > 0:
                professori_votati.append(prof)

        # Crea una lista per i professori da mostrare in classifica
        professori = []

        # Crea una variabile per il form
        form = FormFiltraClassifica()

        # Se è una richiesta di tipo POST significa che è stata scelta una "materia filtro" per la classifica
        if request.method == 'POST':
            # salva il form appena compilato in una variabile
            form = FormFiltraClassifica(request.POST)
            # se il form è valido...
            if form.is_valid():
                # ottieni la materia scelta
                materia = Materia.objects.get(pk=form.cleaned_data['pk_materia'])

                # salva i professori che insegnano questa materia nella lista
                # (se la materia è 'Tutte le materie' riempi la lista con tutti i professori)
                if materia.nome == 'Tutte le materie':
                    for prof in professori_votati:
                        professori.append(prof)
                else:
                    for prof in professori_votati:
                        if prof.materia == materia.nome:
                            professori.append(prof)

        # Altrimenti riempi la lista con tutti i professori
        else:
            for prof in professori_votati:
                professori.append(prof)

        # ordina la lista dei professori
        professori.sort(key=ottieni_punteggio, reverse=True)

        # Aggiungi la lista dei professori e il form tra le variabili da inviare al template
        context['professori'] = professori
        context['form'] = form

        # Crea lista con il numero di prof divisi per gradimento (se alto, medio o basso) da usare nel grafico a torta
        gradimento_basso = 0
        gradimento_medio = 0
        gradimento_alto = 0
        for prof in professori_votati:
            if prof.punteggio_totale < 6:
                gradimento_basso += 1
            elif prof.punteggio_totale >= 6 and prof.punteggio_totale < 8.5:
                gradimento_medio += 1
            else:
                gradimento_alto += 1

        # Aggiungi le tre variabili appena riempite a quelle da inviare al template
        context['gradimento_basso'] = gradimento_basso
        context['gradimento_medio'] = gradimento_medio
        context['gradimento_alto'] = gradimento_alto

        # Crea il dizionario con le medie dei punteggi dei prof divisi per materia
        medie_materie = {}
        for materia in Materia.objects.all():
            if not materia.nome == 'Tutte le materie':
                # Salva i prof di questa materia in una lista
                prof_materia = []
                for prof in professori_votati:
                    if prof.materia == materia.nome:
                        prof_materia.append(prof)

                # Calcola la media dei loro punteggi totali
                media = 0
                i = 0
                for prof in prof_materia:
                    media += prof.punteggio_totale
                    i += 1
                if i != 0:
                    media /= i

                # Aggiungi questa media al dizionario delle medie
                medie_materie[materia.nome] = str(media)

        # Aggiungi il dizionario appena creato alle variabili da inviare al template
        context['medie_materie'] = medie_materie

        return render(request, 'risultati.html', context)
    else:
        # Altrimenti carica la pagina di Accesso Negato
        return render(request, 'no_login.html', {})


# View per il logout
@login_required
def logout(request):
    auth_logout(request)
    return redirect(seleziona_classe)
