from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.ProjectsListView.as_view(), name='project-list-all'),
    path('project/new/', views.ProjectCreateView.as_view(), name='project-create'),
    path('project/<pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/<pk>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('project/<pk>/contributors/', views.project_contributors, name='project-contributors'),
    path('project/<pk>/pulse', views.project_pulse, name='project-pulse'),
    path('project/<pk>/contributors/add-member', views.add_member, name='project-add-member'),
    path('project/<pk>/contributors/<member_id>/delete', views.delete_member, name='project-delete-member'),
    path('project/<pk>/branches/', views.project_branches, name='project-branches'),
    path('project/<pk>/branches/commits/', views.project_commits, name='project-commits'),
    path('project/<pk>/branches/refresh', views.project_refresh_branches, name='project-refresh-branches'),
    path('project/<pk>/settings', views.project_settings, name='project-settings'),
    path('project/<pk>/edit', views.ProjectEditView.as_view(), name='project-edit'),
]
