from django.shortcuts import render
from .models import Organization
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
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

class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
    model = Organization
    template_name = 'app/organization/organization_update.html'
    fields = ['name', 'description']

    # TODO: dodati test_func tako da samo clanovi mogu da menjaju stvari

class OrganizationDeleteView(LoginRequiredMixin, DeleteView):
    model = Organization
    template_name = 'app/organization/organization_confirm_delete.html'
    # TODO: vidi u wiki kako si iskoristio reverse za ovo
    success_url = '/organizations'

    # TODO: dodati test_func za proveru da samo clanovi mogu da obrisu
