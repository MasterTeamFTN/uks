from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.projects, name='app-projects'),
    path('project/new/', views.ProjectCreateView.as_view(), name='project-create'),
    path('project/<pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/<pk>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('project/<pk>/contributors/', views.project_contributors, name='project-contributors'),
    path('project/<pk>/pulse', views.project_pulse, name='project-pulse'),
]
