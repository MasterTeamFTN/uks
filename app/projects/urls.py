from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.projects, name='app-projects'),
    path('project/new/', views.ProjectCreateView.as_view(), name='project-create'),
    path('project/<pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/<pk>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('project/<pk>/contributors/', views.project_contributors, name='project-contributors'),
    path('project/<pk>/branches/', views.project_branches, name='project-branches'),
    path('project/<pk>/branches/commits/', views.project_commits, name='project-commits'),
    path('project/<pk>/branches/refresh', views.project_refresh_branches, name='project-refresh-branches'),
]
