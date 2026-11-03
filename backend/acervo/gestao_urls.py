from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AutorGestaoViewSet,
    CursoGestaoViewSet,
    OrientadorGestaoViewSet,
    PalavraChaveGestaoViewSet,
    TrabalhoGestaoViewSet,
)

router = DefaultRouter()
router.register('trabalhos', TrabalhoGestaoViewSet, basename='gestao-trabalho')
router.register('cursos', CursoGestaoViewSet, basename='gestao-curso')
router.register('orientadores', OrientadorGestaoViewSet, basename='gestao-orientador')
router.register('autores', AutorGestaoViewSet, basename='gestao-autor')
router.register('palavras-chave', PalavraChaveGestaoViewSet, basename='gestao-palavra-chave')

urlpatterns = [path('', include(router.urls))]
