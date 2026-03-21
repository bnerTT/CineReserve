from rest_framework import serializers
from .models import Filme, Sala, Assento, Sessao, Reserva

class AssentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assento
        fields = ['id', 'sala', 'fileira', 'numero']

class SessaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessao
        fields = ['id', 'filme', 'sala', 'horario_inicio']

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'usuario', 'sessao', 'assento', 'status', 'criada_em']
        read_only_fields = ['status', 'criada_em']

    def validate(self, data):
        sessao = data['sessao']
        assento = data['assento']

        if assento.sala != sessao.sala:
                raise serializers.ValidationError("O assento selecionado não pertence à sala da sessão.")
            
        if Reserva.objects.filter(sessao=sessao, assento=assento).exists():
                raise serializers.ValidationError("O assento já está reservado para esta sessão.")
            
        return data
        

class FilmeSerializer(serializers.ModelSerializer):
    sessoes = SessaoSerializer(many=True, read_only=True)

    class Meta:
        model = Filme
        fields = ['id', 'titulo', 'sinopse', 'duracao', 'em_cartaz', 'sessoes']

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ['id', 'nome']

