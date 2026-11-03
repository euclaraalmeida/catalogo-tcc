from rest_framework import serializers
from django.utils import timezone

from .models import Autor, Curso, Orientador, PalavraChave, Trabalho


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


class CursoGestaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['id', 'nome', 'sigla']


class OrientadorGestaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orientador
        fields = ['id', 'nome', 'titulacao', 'email_institucional']


class AutorGestaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nome', 'email']


class PalavraChaveGestaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalavraChave
        fields = ['id', 'termo']


class TrabalhoGestaoSerializer(serializers.ModelSerializer):
    cadastrado_por = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Trabalho
        fields = [
            'id', 'titulo', 'resumo', 'ano', 'data_defesa', 'nota', 'situacao',
            'link_pdf', 'curso', 'orientador', 'coorientador', 'autores',
            'palavras_chave', 'cadastrado_por',
        ]

    def validate(self, attrs):
        ano = attrs.get('ano', getattr(self.instance, 'ano', None))
        situacao = attrs.get('situacao', getattr(self.instance, 'situacao', None))
        nota = attrs.get('nota', getattr(self.instance, 'nota', None))
        data_defesa = attrs.get('data_defesa', getattr(self.instance, 'data_defesa', None))
        autores = attrs.get('autores', list(self.instance.autores.all()) if self.instance else [])
        erros = {}
        if ano and ano > timezone.localdate().year:
            erros['ano'] = 'O ano não pode ser maior que o ano corrente.'
        if situacao == Trabalho.Situacao.PUBLICADO:
            if nota is None:
                erros['nota'] = 'Um trabalho publicado precisa ter nota.'
            if not data_defesa:
                erros['data_defesa'] = 'Um trabalho publicado precisa ter data de defesa.'
        if not 1 <= len(autores) <= 2:
            erros['autores'] = 'O trabalho deve ter um ou dois autores.'
        titulo = attrs.get('titulo', getattr(self.instance, 'titulo', None))
        curso = attrs.get('curso', getattr(self.instance, 'curso', None))
        if titulo and curso and ano and Trabalho.objects.exclude(pk=getattr(self.instance, 'pk', None)).filter(
            titulo__iexact=titulo, curso=curso, ano=ano,
        ).exists():
            erros['titulo'] = 'Já existe trabalho com este título, curso e ano.'
        if erros:
            raise serializers.ValidationError(erros)
        return attrs

    def create(self, validated_data):
        autores = validated_data.pop('autores')
        palavras_chave = validated_data.pop('palavras_chave', [])
        trabalho = Trabalho.objects.create(**validated_data)
        trabalho.autores.set(autores)
        trabalho.palavras_chave.set(palavras_chave)
        return trabalho

    def update(self, instance, validated_data):
        autores = validated_data.pop('autores', None)
        palavras_chave = validated_data.pop('palavras_chave', None)
        for campo, valor in validated_data.items():
            setattr(instance, campo, valor)
        instance.full_clean(exclude=['autores', 'palavras_chave'])
        instance.save()
        if autores is not None:
            instance.autores.set(autores)
        if palavras_chave is not None:
            instance.palavras_chave.set(palavras_chave)
        return instance
