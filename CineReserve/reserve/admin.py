from django.contrib import admin
from .models import Filme, Sala, Sessao, AssentoReservado


@admin.register(Filme)
class FilmeAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'duracao', 'em_cartaz')
	list_filter = ('em_cartaz',)
	search_fields = ('titulo',)


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
	list_display = ('nome', 'fileiras', 'colunas')
	search_fields = ('nome',)


@admin.register(Sessao)
class SessaoAdmin(admin.ModelAdmin):
	list_display = ('filme', 'sala', 'horario_inicio', 'assentos_disponiveis')
	list_filter = ('sala', 'filme')
	search_fields = ('filme__titulo', 'sala__nome')


@admin.register(AssentoReservado)
class AssentoReservadoAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'sessao', 'fileira', 'coluna', 'status', 'data_reserva')
	list_filter = ('status', 'sessao', 'sessao__filme', 'sessao__sala')
	search_fields = ('usuario__username', 'sessao__filme__titulo', 'sessao__sala__nome')
	readonly_fields = ('data_reserva',)
