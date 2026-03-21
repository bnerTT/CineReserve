from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FilmeViewSet, SessaoViewSet, ReservaViewSet

router = DefaultRouter()
router.register(r'filmes', FilmeViewSet, basename='filme')
router.register(r'sessoes', SessaoViewSet, basename='sessao')
router.register(r'reservas', ReservaViewSet, basename='reserva')

urlpatterns = [
    path('api/', include(router.urls)),
]
