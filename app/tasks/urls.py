from django.urls import path
from . import views

urlpatterns = [
    path('project/<project_pk>/task/', views.task_list_view, name='task-list'),
    path('project/<project_pk>/task/new/', views.TaskCreateView.as_view(), name='task-create'),
    path('project/<project_pk>/task/<pk>/', views.task_detail_view, name='task-detail'),
    path('project/<project_pk>/task/<pk>/close/', views.TaskDeleteView.as_view(), name='task-close'),

]
