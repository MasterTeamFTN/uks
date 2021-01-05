from django.contrib import admin
from django.urls import path
from .views import (
    ProjectDetailView,
    ProjectDeleteView,
    ProjectCreateView
)
from . import views

urlpatterns = [
    path('', views.home, name='app-home'),
    path('about/', views.about, name='app-about'),
    path('projects/', views.projects, name='app-projects'),
    path('project-detail/<pk>', ProjectDetailView.as_view(), name='project-detail'),
    path('project/<pk>/delete', ProjectDeleteView.as_view(), name='project-delete'),
    path('project/new/', ProjectCreateView.as_view(), name='project-create'),
]
