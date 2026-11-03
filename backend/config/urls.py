from django.urls import include, path


urlpatterns = [
    path('api/v1/publico/', include('acervo.urls')),
]
