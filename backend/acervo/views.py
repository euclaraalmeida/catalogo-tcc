from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer

from .filters import TrabalhoFilter
from .models import Trabalho
from .serializers import TrabalhoDetalhePublicoSerializer, TrabalhoPublicoSerializer


@extend_schema_view(
    list=extend_schema(summary='Lista trabalhos publicados', description='Lista paginada de trabalhos publicados. Aceita busca, filtros por ano/curso/palavra-chave e ordenação por ano/título.'),
    retrieve=extend_schema(summary='Detalha trabalho publicado', description='Retorna o resumo completo e palavras-chave. Trabalhos não publicados retornam 404.'),
)
class TrabalhoPublicoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trabalho.objects.filter(situacao=Trabalho.Situacao.PUBLICADO).select_related(
        'curso', 'orientador', 'coorientador',
    ).prefetch_related('autores', 'palavras_chave')
    serializer_class = TrabalhoPublicoSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TrabalhoFilter
    search_fields = ['titulo', 'resumo', 'autores__nome', 'orientador__nome']
    ordering_fields = ['ano', 'titulo']
    ordering = ['-ano', 'titulo', 'pk']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TrabalhoDetalhePublicoSerializer
        return TrabalhoPublicoSerializer


@extend_schema(
    summary='Estatísticas públicas',
    description='Calcula no banco totais de trabalhos publicados por ano e curso e os cinco orientadores com mais trabalhos.',
    responses=inline_serializer(name='EstatisticasPublicas', fields={
        'trabalhos_por_ano': serializers.ListField(child=serializers.DictField()),
        'trabalhos_por_curso': serializers.ListField(child=serializers.DictField()),
        'orientadores_com_mais_trabalhos': serializers.ListField(child=serializers.DictField()),
    }),
)
@api_view(['GET'])
@permission_classes([AllowAny])
def estatisticas(request):
    trabalhos = Trabalho.objects.filter(situacao=Trabalho.Situacao.PUBLICADO)
    por_ano = trabalhos.values('ano').annotate(total=Count('pk')).order_by('ano')
    por_curso = trabalhos.values('curso_id', 'curso__nome', 'curso__sigla').annotate(total=Count('pk')).order_by('curso__nome')
    orientadores = trabalhos.values('orientador__nome').annotate(total=Count('pk')).order_by('-total', 'orientador__nome')[:5]
    return Response({
        'trabalhos_por_ano': list(por_ano),
        'trabalhos_por_curso': list(por_curso),
        'orientadores_com_mais_trabalhos': list(orientadores),
    })


class GestaoViewSet(viewsets.ModelViewSet):
    permission_classes = []

    def perform_create(self, serializer):
        serializer.save(cadastrado_por=self.request.user)


from .models import Autor, Curso, Orientador, PalavraChave
from .serializers import (
    AutorGestaoSerializer, CursoGestaoSerializer, OrientadorGestaoSerializer,
    PalavraChaveGestaoSerializer, TrabalhoGestaoSerializer,
)
from rest_framework.permissions import IsAuthenticated


class CursoGestaoViewSet(GestaoViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoGestaoSerializer
    permission_classes = [IsAuthenticated]


class OrientadorGestaoViewSet(GestaoViewSet):
    queryset = Orientador.objects.all()
    serializer_class = OrientadorGestaoSerializer
    permission_classes = [IsAuthenticated]


class AutorGestaoViewSet(GestaoViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorGestaoSerializer
    permission_classes = [IsAuthenticated]


class PalavraChaveGestaoViewSet(GestaoViewSet):
    queryset = PalavraChave.objects.all()
    serializer_class = PalavraChaveGestaoSerializer
    permission_classes = [IsAuthenticated]


class TrabalhoGestaoViewSet(GestaoViewSet):
    queryset = Trabalho.objects.all().select_related('curso', 'orientador', 'coorientador').prefetch_related('autores', 'palavras_chave')
    serializer_class = TrabalhoGestaoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(cadastrado_por=self.request.user)
