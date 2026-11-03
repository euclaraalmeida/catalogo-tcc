from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('api/token/', obtain_auth_token, name='api-token'),
    path('api/v1/publico/', include('acervo.urls')),
    path('api/gestao/', include('acervo.gestao_urls')),
]
