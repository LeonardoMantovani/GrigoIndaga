from django.shortcuts import render
from .models import Classe


# View per la selezione della classe
def seleziona_classe(request):
    classi = Classe.objects.all()
    return render(request, 'seleziona_classe.html', {'classi': classi})
