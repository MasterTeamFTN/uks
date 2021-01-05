from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='app-home'),
    path('about/', views.about, name='app-about'),
    path('projects/', views.projects, name='app-projects'),
    path('project/<pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/<pk>/delete', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('project/new/', views.ProjectCreateView.as_view(), name='project-create'),
    
    path('project/<project_pk>/wiki/', views.wikis_list_view, name='wiki-list'),
    path('project/<project_pk>/wiki/new/', views.WikiCreateView.as_view(), name='wiki-create'),
    path('project/<project_pk>/wiki/<pk>/', views.WikiDetailView.as_view(), name='wiki-detail'),
    path('project/<project_pk>/wiki/<pk>/delete/', views.WikiDeleteView.as_view(), name='wiki-delete'),
    path('project/<project_pk>/wiki/<pk>/update/', views.WikiUpdateView.as_view(), name='wiki-update'),
    path('project/<project_pk>/wiki/<pk>/history/', views.wiki_versions_list_view, name='wiki-history'),
]
