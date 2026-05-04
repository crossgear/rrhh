from django.urls import path

from .views import InterinatoCreateView, InterinatoUpdateView, InterinatoDeleteView

urlpatterns = [
    path('persona/<int:persona_pk>/crear/', InterinatoCreateView.as_view(), name='interinato-create'),
    path('<int:pk>/editar/', InterinatoUpdateView.as_view(), name='interinato-update'),
    path('<int:pk>/eliminar/', InterinatoDeleteView.as_view(), name='interinato-delete'),
]
