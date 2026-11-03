from django_filters import rest_framework as filters

from .models import Trabalho


class TrabalhoFilter(filters.FilterSet):
    palavra_chave = filters.CharFilter(field_name='palavras_chave__termo', lookup_expr='iexact')

    class Meta:
        model = Trabalho
        fields = ['ano', 'curso', 'palavra_chave']
