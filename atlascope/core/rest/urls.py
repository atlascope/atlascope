from django.urls import path

from atlascope.core.rest import views

urlpatterns = [
    path('investigations/', views.InvestigationList.as_view(), name='investigation-list'),
    path(
        'investigation/<int:pk>/', views.InvestigationDetail.as_view(), name='investigation-detail'
    ),
    path('context-map/<int:pk>/', views.ContextMapDetail.as_view(), name='context-map-detail'),
    path(
        'connections-map/<int:pk>/',
        views.ConnectionsMapDetail.as_view(),
        name='connections-map-detail',
    ),
    path('datasets/', views.DatasetList.as_view(), name='dataset-list'),
    path('dataset/<int:pk>/', views.DatasetDetail.as_view(), name='dataset-detail'),
    path('pins/', views.PinList.as_view(), name='pin-list'),
    path('pin/<int:pk>/', views.PinDetail.as_view(), name='pin-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('', views.APIRoot.as_view(), name='api-root'),
]
