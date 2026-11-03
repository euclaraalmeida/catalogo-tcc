from rest_framework import serializers

from .models import Curso, Trabalho


class CursoPublicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['nome', 'sigla']


class TrabalhoPublicoSerializer(serializers.ModelSerializer):
    curso = CursoPublicoSerializer(read_only=True)
    orientador = serializers.StringRelatedField()
    autores = serializers.StringRelatedField(many=True)

    class Meta:
        model = Trabalho
        fields = ['id', 'titulo', 'ano', 'curso', 'orientador', 'autores']


class TrabalhoDetalhePublicoSerializer(TrabalhoPublicoSerializer):
    coorientador = serializers.StringRelatedField()
    palavras_chave = serializers.StringRelatedField(many=True)

    class Meta(TrabalhoPublicoSerializer.Meta):
        fields = TrabalhoPublicoSerializer.Meta.fields + [
            'resumo', 'data_defesa', 'link_pdf', 'coorientador', 'palavras_chave',
        ]
