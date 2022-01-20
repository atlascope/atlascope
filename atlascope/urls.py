from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from atlascope.core.rest.endpoints import (
    AtlascopeConfigView,
    DatasetViewSet,
    InvestigationViewSet,
    PinViewSet,
    UserViewSet,
)

# OpenAPI generation
schema_view = get_schema_view(
    openapi.Info(title='Atlascope', default_version='v1', description=''),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter(trailing_slash=False)

for model_name, viewset in [
    ('user', UserViewSet),
    ('investigation', InvestigationViewSet),
    ('dataset', DatasetViewSet),
    ('pin', PinViewSet),
]:
    router.register(f'{model_name}s', viewset, basename=model_name)

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('admin/', admin.site.urls),
    path('api/v1/s3-upload/', include('s3_file_field.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/configuration/', AtlascopeConfigView.as_view()),
    path('api/docs/redoc/', schema_view.with_ui('redoc'), name='docs-redoc'),
    path('api/docs/swagger/', schema_view.with_ui('swagger'), name='docs-swagger'),
    path('api/v1/', include('atlascope.core.rest.endpoints.tile_endpoints')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
