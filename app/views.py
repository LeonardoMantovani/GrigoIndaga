from django.shortcuts import render


# View per la selezione della classe
def seleziona_classe(request):
    return render(request, 'seleziona_classe.html', {})
