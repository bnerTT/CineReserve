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

    def __str__(self):
        return self.nome
    
class Assento(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    fileira = models.CharField(max_length=5)
    numero = models.CharField(max_length=5)

    class Meta:
        unique_together = ('sala', 'fileira', 'numero')

    def __str__(self):
        return f"{self.sala.nome} - {self.fileira}{self.numero}"
    
class Sessao(models.Model):
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='sessoes')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    horario_inicio = models.DateTimeField()

    def __str__(self):
        return f"{self.filme.titulo} - {self.sala.nome} - {self.horario_inicio}"
    
class Reserva(models.Model):
    STATUS_CHOICES = (
        ('R', 'Reservado'),
        ('F', 'Fechado'),
        ('D', 'Disponivel'),
    )
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    sessao = models.ForeignKey(Sessao, on_delete=models.CASCADE)
    assento = models.ForeignKey(Assento, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='D')
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sessao', 'assento')

    def __str__(self):
        return f"Reserva de {self.usuario.username} para {self.sessao.filme.titulo} - {self.assento}"