from django.urls import path
from . import views

urlpatterns = [
    path('organizations/', views.AllOrganizationsListView.as_view(), name='organization-list-all'),
    path('organizations/new/', views.OrganizationCreateView.as_view(), name='organization-create'),
    path('organizations/<pk>/', views.OrganizationDetailView.as_view(), name='organization-detail'),
]
