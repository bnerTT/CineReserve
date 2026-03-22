from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    FilmeViewSet,
    SalaViewSet,
    SessaoViewSet,
    AssentoReservadoViewSet,
    RegistroUsuarioViewSet,
)

router = DefaultRouter()
router.register(r'filmes', FilmeViewSet, basename='filme')
router.register(r'salas', SalaViewSet, basename='sala')
router.register(r'sessoes', SessaoViewSet, basename='sessao')
router.register(r'reservas', AssentoReservadoViewSet, basename='assento')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/register/', RegistroUsuarioViewSet.as_view(), name='auth_registrar'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]