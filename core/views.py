from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# esse é um metodo de redirecionar mas vou utlizar o que é diretamente pela url
# def index(req):
#  return redirect('/agenda/')


def Eventos(req, tituloEvento):
    return HttpResponse(f'Nome do evento: {tituloEvento} ')


def login_user(req):
    return render(req, 'login.html')


def logout_user(req):
    logout(req)
    return redirect('/')  # quando entrar na função logout ele vai me recaminhar para o index


def submit_login(req):
    if req.POST:
        username = req.POST.get('username')
        password = req.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(req, usuario)
            return redirect('/')
        else:
            messages.error(req, "Usuario ou senha invalido!")

    return redirect('/')


@login_required(login_url='/login/')  # pra quando o usuario nao estiver autenticado ele me levar para essa rota
def lista_eventos(req):
    usuario = req.user
    evento = Evento.objects.filter(usuario=usuario)
    dados = {'eventos': evento}
    return render(req, 'agenda.html', dados)


@login_required(login_url='/login/')
def evento(req):
    return render(req, 'evento.html')


@login_required(login_url='/login/')
def submit_evento(req):
    if req.POST:
        titulo = req.POST.get('titulo')
        data_evento = req.POST.get('data_evento')
        descricao = req.POST.get('descricao')
        local = req.POST.get('local')
        usuario = req.user
        Evento.objects.create(titulo=titulo, data_evento=data_evento,
                              descricao=descricao, local=local, usuario=usuario)

    return redirect('/')

# Create your views here.
