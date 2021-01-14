from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseBadRequest
from .models import Organization
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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

@login_required
def add_member(request, pk):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    username = request.POST['member_username']
    print(username)

    try:
        user = User.objects.get(username=username)
    except:
        messages.warning(request, f'Error! User {username} doesn\'t exist.')
        return redirect('organization-detail', pk)

    organization = Organization.objects.get(pk=pk)

    if user in organization.members.all():
        messages.warning(request, f'User {username} is already in the members list.')
        return redirect('organization-detail', pk)

    organization.members.add(user)

    messages.success(request, f'User {username} has been added to the members list.')
    return redirect('organization-detail', pk)
