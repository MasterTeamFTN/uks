from django.urls import path
from . import views

urlpatterns = [
    path('project/<project_pk>/milestone/new/', views.MilestoneCreateView.as_view(), name='milestone-create'),
    path('project/<project_pk>/milestone/<pk>/delete/', views.MilestoneDeleteView.as_view(), name='milestone-delete'),
    path('project/<project_pk>/milestone/<pk>/update/', views.MilestoneUpdateView.as_view(), name='milestone-update'),
    path('project/<project_pk>/milestone/', views.milestone_list_view, name='milestone-list'),
    path('project/<project_pk>/milestone/<pk>/', views.MilestoneDetailView.as_view(), name='milestone-detail'),

]
