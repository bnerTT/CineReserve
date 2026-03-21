from django.contrib import admin
from .models import Filme, Sala, Assento, Sessao, Reserva

@admin.register(Filme)
class FilmeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'duracao', 'em_cartaz')
    list_filter = ('em_cartaz',)
    search_fields = ('titulo',)

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Assento)
class AssentoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'fileira', 'sala')
    list_filter = ('sala', 'fileira')
    search_fields = ('numero', 'fileira', 'sala__nome')

@admin.register(Sessao)
class SessaoAdmin(admin.ModelAdmin):
    list_display = ('filme', 'sala', 'horario_inicio')
    list_filter = ('filme', 'sala')
    search_fields = ('filme__titulo',)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'sessao', 'assento', 'status', 'criada_em')
    list_filter = ('status', 'sessao')
    search_fields = ('usuario__username', 'sessao__filme__titulo')
    readonly_fields = ('criada_em',)