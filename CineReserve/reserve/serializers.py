from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Filme, Sala, Sessao, AssentoReservado

User = get_user_model()

class FilmeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filme
        fields = '__all__'

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'

class SessaoSerializer(serializers.ModelSerializer):
    assentos_disponiveis = serializers.ReadOnlyField()

    filme_titulo = serializers.ReadOnlyField(source='filme.titulo')
    sala_nome = serializers.ReadOnlyField(source='sala.nome')

    sala_colunas = serializers.ReadOnlyField(source='sala.colunas')
    sala_fileiras = serializers.ReadOnlyField(source='sala.fileiras')
    
    class Meta:
        model = Sessao
        fields = ['id',
                  'sala', 
                  'sala_nome',
                  'filme',
                 'filme_titulo',
                 'assentos_disponiveis',
                  'horario_inicio',
                    'sala_colunas',
                    'sala_fileiras',
                  ]

class AssentoReservadoSerializer(serializers.ModelSerializer):
    fileira = serializers.CharField(max_length=2)

    class Meta:
        model = AssentoReservado
        fields = '__all__'
        read_only_fields = ['usuario', 'data_reserva']

    def validate(self, attrs):
        sessao = attrs.get('sessao')
        coluna = attrs.get('coluna')
        fileira = attrs.get('fileira')

        if sessao is None:
            return attrs

        if coluna is None or coluna < 1 or coluna > sessao.sala.colunas:
            raise serializers.ValidationError("Coluna inválida para esta sessão.")

        if not fileira:
            raise serializers.ValidationError("Fileira é obrigatória.")

        fileira_normalizada = fileira.strip().upper()
        if len(fileira_normalizada) != 1 or not fileira_normalizada.isalpha():
            raise serializers.ValidationError("Fileira deve ser uma única letra (ex: A, B, C).")

        indice_fileira = ord(fileira_normalizada) - ord('A') + 1
        if indice_fileira < 1 or indice_fileira > sessao.sala.fileiras:
            raise serializers.ValidationError("Fileira inválida para esta sessão.")

        conflito = AssentoReservado.objects.filter(
            sessao=sessao,
            fileira=fileira_normalizada,
            coluna=coluna,
        )
        if self.instance is not None:
            conflito = conflito.exclude(pk=self.instance.pk)

        if conflito.exists():
            raise serializers.ValidationError("Este assento já está reservado para esta sessão.")

        attrs['fileira'] = fileira_normalizada
        return attrs


class RegistroUsuarioSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'senha']

    def validate(self, attrs):
        senha = attrs.get('senha')
        password = attrs.get('password')
        senha_final = password or senha

        if not senha_final:
            raise serializers.ValidationError(
                {'password': 'Informe password ou senha para criar a conta.'}
            )

        attrs['password'] = senha_final
        attrs.pop('senha', None)
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=password,
        )