from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento

#esse é um metodo de redirecionar mas vou utlizar o que é diretamente pela url
#def index(req):
  #  return redirect('/agenda/')


def Eventos(req, tituloEvento):
    return HttpResponse(f'Nome do evento: {tituloEvento} ')


def lista_eventos(req):
    evento = Evento.objects.all()
    dados = {'eventos': evento}
    return render(req, 'agenda.html', dados)

# Create your views here.
