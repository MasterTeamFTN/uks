from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from .models import Organization
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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

class OrganizationDetailView(DetailView):
    model = Organization
    template_name = 'app/organization/organization_detail.html'

class OrganizationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Organization
    template_name = 'app/organization/organization_update.html'
    fields = ['name', 'description']

    def test_func(self):
        org = self.get_object()
        return self.request.user in org.members.all()

class OrganizationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Organization
    template_name = 'app/organization/organization_confirm_delete.html'
    success_url = '/organizations'

    def test_func(self):
        org = self.get_object()
        return self.request.user in org.members.all()

@login_required
def add_member(request, pk):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    organization = Organization.objects.get(pk=pk)

    if request.user not in organization.members.all():
        return HttpResponseForbidden('403 forbidden')

    username = request.POST['member_username']

    try:
        user = User.objects.get(username=username)
    except:
        messages.warning(request, f'Error! User {username} doesn\'t exist.')
        return redirect('organization-detail', pk)

    if user in organization.members.all():
        messages.warning(request, f'User {username} is already in the members list.')
        return redirect('organization-detail', pk)

    organization.members.add(user)

    messages.success(request, f'User {username} has been added to the members list.')
    return redirect('organization-detail', pk)

@login_required
def delete_member(request, pk, member_id):
    organization = Organization.objects.get(pk=pk)

    if request.user not in organization.members.all():
        return HttpResponseForbidden('403 forbidden')

    try:
        user = User.objects.get(pk=member_id)
    except:
        messages.warning(request, f'Error! User {username} doesn\'t exist.')
        return redirect('organization-detail', pk)

    username = user.username
    organization.members.remove(user)

    messages.success(request, f'User {username} has been removed from organization.')
    return redirect('organization-detail', pk)
