from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import APIRootView, DefaultRouter

from .views import TrabalhoPublicoViewSet, estatisticas


class RaizPublica(APIRootView):
    permission_classes = [AllowAny]


class RouterPublico(DefaultRouter):
    APIRootView = RaizPublica


router = RouterPublico()
router.register('trabalhos', TrabalhoPublicoViewSet, basename='trabalho-publico')

urlpatterns = [
    path('estatisticas/', estatisticas, name='estatisticas'),
    path('', include(router.urls)),
]
