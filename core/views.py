
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse


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
    data_atual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario,
                                   data_evento__gt=data_atual)
    # data_evento__gt = data_atual o comando __gt traz datas acima da data atual e o lt abaixo
    dados = {'eventos': evento}
    return render(req, 'agenda.html', dados)


@login_required(login_url='/login/')
def evento(req):
    id_evento = req.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)

    return render(req, 'evento.html', dados)


@login_required(login_url='/login/')
def submit_evento(req):
    if req.POST:
        titulo = req.POST.get('titulo')
        data_evento = req.POST.get('data_evento')
        descricao = req.POST.get('descricao')
        local = req.POST.get('local')
        usuario = req.user
        id_evento = req.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            # 2Formas de como fazer o update

            # 1forma
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.local = local
                evento.save()

                # 2forma
        # Evento.objects.filter(id=id_evento).update(titulo=titulo, data_evento=data_evento,
        #            descricao=descricao, local=local)
        else:
            Evento.objects.create(titulo=titulo, data_evento=data_evento,
                                  descricao=descricao, local=local, usuario=usuario)

    return redirect('/')


@login_required(login_url='/login/')
def delete_evento(req, id_evento):
    usuario = req.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')


def json_lista_evento(req, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')

    return JsonResponse(list(evento), safe=False)

# Create your views here.
