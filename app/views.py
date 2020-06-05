from django.shortcuts import render


# Create your views here.
def seleziona_classe(request):
    return render(request, 'seleziona_classe.html', {})
