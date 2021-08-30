from django.db import models
from django.contrib.auth.models import User


class Evento(models.Model):
    titulo = models.CharField(max_length=100)  # no maximo 100 carcteres
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(verbose_name='Data do Evento')
    data_criacao = models.DateTimeField(auto_now=True)  # o auto_now insere a hora atual automaticamente
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'evento'  # exigindo que minha tabela se chame "evento"

    def __str__(self):
        return self.titulo

    ##migro a classe para o banco de dados para ela virar uma tabela e especifico o nome do meu app

# Create your models here.
