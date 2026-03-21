from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Filme, Sessao, Reserva
from .serializers import FilmeSerializer, SessaoSerializer, ReservaSerializer

# Create your views here.
class FilmeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Filme.objects.filter(em_cartaz=True)
    serializer_class = FilmeSerializer

class SessaoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sessao.objects.all()
    serializer_class = SessaoSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user)