from django.shortcuts import render
from .models import Organization
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

class AllOrganizationsListView(ListView):
    model = Organization
    template_name = 'app/organization/organization_list_all.html'
    context_object_name = 'organizations'

class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    template_name = 'app/organization/organization_form.html'
    fields = ['name', 'description']

    def form_valid(self, form):
        # User that creates org. is first member
        # form.instance.members.append(self.request.user)
        return super().form_valid(form)

class OrganizationDetailView(DetailView):
    model = Organization
    template_name = 'app/organization/organization_detail.html'
