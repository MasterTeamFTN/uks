from django.urls import path
from . import views

urlpatterns = [
    path('project/<project_pk>/task/', views.task_list_view, name='task-list'),
    path('project/<project_pk>/board/', views.board_view, name='board'),
    path('tasks', views.my_task_list_view, name='my-list'),
    path('project/<project_pk>/task/new/', views.TaskCreateView.as_view(), name='task-create'),
    path('project/<project_pk>/task/<pk>/', views.task_detail_view, name='task-detail'),
    path('project/<project_pk>/task/<pk>/close', views.close_task, name='close-task'),
    path('project/<project_pk>/task/<pk>/progress', views.progress_task, name='progress-task'),
    path('project/<project_pk>/task/<pk>/review', views.review_task, name='review-task'),
    path('project/<project_pk>/task/<pk>/todo', views.todo_task, name='todo-task'),
    path('project/<project_pk>/task/<pk>/done', views.done_task, name='done-task'),
    path('project/<project_pk>/task/<pk>/reopen', views.reopen_task, name='reopen-task'),
    path('project/<project_pk>/task/<pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
]
