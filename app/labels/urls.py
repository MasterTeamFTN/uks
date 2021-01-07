from django.urls import path
from . import views

urlpatterns = [
    path('project/<project_pk>/label/new/', views.LabelCreateView.as_view(), name='label-create'),
    path('project/<project_pk>/label/<pk>/delete/', views.LabelDeleteView.as_view(), name='label-delete'),
    path('project/<project_pk>/label/<pk>/update/', views.LabelUpdateView.as_view(), name='label-update'),
    path('project/<project_pk>/label/', views.label_list_view, name='label-list'),
]