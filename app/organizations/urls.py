from django.urls import path
from . import views

urlpatterns = [
    path('organizations/', views.AllOrganizationsListView.as_view(), name='organization-list-all'),
    path('organizations/new/', views.OrganizationCreateView.as_view(), name='organization-create'),
    path('organizations/<pk>/', views.OrganizationDetailView.as_view(), name='organization-detail'),
    path('organizations/<pk>/add-project', views.OrganizationProjectCreateView.as_view(), name='organization-add-project'),
    path('organizations/<pk>/edit/', views.OrganizationUpdateView.as_view(), name='organization-edit'),
    path('organizations/<pk>/delete/', views.OrganizationDeleteView.as_view(), name='organization-delete'),
    path('organizations/<pk>/member/add/', views.add_member, name='organization-add-member'),
    path('organizations/<pk>/member/<member_id>/delete/', views.delete_member, name='organization-delete-member'),
]
