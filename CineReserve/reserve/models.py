from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Filme(models.Model):
    titulo = models.CharField(max_length=100)
    sinopse = models.TextField()
    duracao = models.IntegerField()
    em_cartaz = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo
    
class Sala(models.Model):
    nome = models.CharField(max_length=50)
    colunas = models.PositiveIntegerField(default=10)
    fileiras = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.nome

class Sessao(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='sessoes')
    horario_inicio = models.DateTimeField()

    @property
    def assentos_disponiveis(self):
        return (self.sala.colunas * self.sala.fileiras) - self.reservas.count()

    def __str__(self):
        return f"{self.filme.titulo} - {self.sala.nome} - {self.horario_inicio}"
    

class AssentoReservado(models.Model):

    STATUS_CHOICES = (
        ('R', 'Reservado'),
        ('P', 'Pago')
    )

    sessao = models.ForeignKey(Sessao, related_name='reservas', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fileira = models.CharField(max_length=2)
    coluna = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='R')
    data_reserva = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sessao', 'fileira', 'coluna')

    def __str__(self):
        return f"{self.usuario.username} - {self.sessao.filme.titulo} - Fileira {self.fileira} Coluna {self.coluna} - Status: {self.get_status_display()}"
    