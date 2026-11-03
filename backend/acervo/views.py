from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filters import TrabalhoFilter
from .models import Trabalho
from .serializers import TrabalhoDetalhePublicoSerializer, TrabalhoPublicoSerializer


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


@api_view(['GET'])
@permission_classes([AllowAny])
def estatisticas(request):
    trabalhos = Trabalho.objects.filter(situacao=Trabalho.Situacao.PUBLICADO)
    por_ano = trabalhos.values('ano').annotate(total=Count('pk')).order_by('ano')
    por_curso = trabalhos.values('curso__nome', 'curso__sigla').annotate(total=Count('pk')).order_by('curso__nome')
    orientadores = trabalhos.values('orientador__nome').annotate(total=Count('pk')).order_by('-total', 'orientador__nome')[:5]
    return Response({
        'trabalhos_por_ano': list(por_ano),
        'trabalhos_por_curso': list(por_curso),
        'orientadores_com_mais_trabalhos': list(orientadores),
    })
