from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from atlascope.core.rest.endpoints import (
    DatasetViewSet,
    DetectedStructureViewSet,
    InvestigationViewSet,
    JobViewSet,
    PinViewSet,
    get_similar_nuclei,
)

# OpenAPI generation
schema_view = get_schema_view(
    openapi.Info(title='Atlascope', default_version='v1', description=''),
    public=True,
)

router = routers.DefaultRouter(trailing_slash=False)

for model_name, viewset in [
    ('investigation', InvestigationViewSet),
    ('dataset', DatasetViewSet),
    ('detected-structure', DetectedStructureViewSet),
    ('pin', PinViewSet),
    ('job', JobViewSet),
]:
    router.register(f'{model_name}s', viewset, basename=model_name)

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/docs/redoc/', schema_view.with_ui('redoc'), name='docs-redoc'),
    path('api/docs/swagger/', schema_view.with_ui('swagger'), name='docs-swagger'),
    path('api/v1/', include('atlascope.core.rest.endpoints.tile_endpoints')),
    path('api/v1/similar-nuclei/<int:dataset>/<str:x>/<str:y>/', get_similar_nuclei),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
