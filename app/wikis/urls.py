from django.urls import path
from . import views

urlpatterns = [
    path('project/<project_pk>/wiki/', views.wikis_list_view, name='wiki-list'),
    path('project/<project_pk>/wiki/new/', views.WikiCreateView.as_view(), name='wiki-create'),
    path('project/<project_pk>/wiki/<pk>/', views.WikiDetailView.as_view(), name='wiki-detail'),
    path('project/<project_pk>/wiki/<pk>/delete/', views.WikiDeleteView.as_view(), name='wiki-delete'),
    path('project/<project_pk>/wiki/<pk>/update/', views.WikiUpdateView.as_view(), name='wiki-update'),
    path('project/<project_pk>/wiki/<pk>/history/', views.wiki_versions_list_view, name='wiki-history'),
]
