from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .models import Filme, Sala, Sessao, AssentoReservado
from .serializers import (
    FilmeSerializer,
    SalaSerializer,
    SessaoSerializer,
    AssentoReservadoSerializer,
    RegistroUsuarioSerializer,
)

User = get_user_model()

class FilmeViewSet(viewsets.ModelViewSet):
    queryset = Filme.objects.all()
    serializer_class = FilmeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'sessoes']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(detail=True, methods=['get'])
    def sessoes(self, request, pk=None):
        queryset = Sessao.objects.filter(filme_id=pk).order_by('horario_inicio')
        serializer = SessaoSerializer(queryset, many=True)
        return Response(serializer.data)

class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class SessaoViewSet(viewsets.ModelViewSet):
    queryset = Sessao.objects.all()
    serializer_class = SessaoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'assentos_ocupados']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        queryset = Sessao.objects.all()
        filme_id = self.request.query_params.get('filme')

        if filme_id:
            queryset = queryset.filter(filme_id=filme_id)

        return queryset

    @action(detail=True, methods=['get'])
    def assentos_ocupados(self, request, pk=None):
        sessao = self.get_object()
        reservas = sessao.reservas.all()

        ocupados = [
            {
                'fileira': reserva.fileira,
                'coluna': reserva.coluna,
                'status': reserva.status
            }
            for reserva in reservas
        ]

        return Response(ocupados)

class AssentoReservadoViewSet(viewsets.ModelViewSet):
    queryset = AssentoReservado.objects.all()
    serializer_class = AssentoReservadoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return AssentoReservado.objects.all()
        return AssentoReservado.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class RegistroUsuarioViewSet(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistroUsuarioSerializer
    permission_classes = [AllowAny]