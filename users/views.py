from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from app.projects.models import Commit, Project
from app.organizations.models import Organization

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'You account has been created')
            return redirect('users-login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def editProfile(request):
    if request.method == 'POST':
        userForm = UserUpdateForm(request.POST, instance=request.user)
        profileForm = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('edit-profile')

    else:
        userForm = UserUpdateForm(instance=request.user)
        profileForm = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'userForm': userForm,
        'profileForm': profileForm
    }

    return render(request, 'users/edit_profile.html', context)

@login_required
def profile(request):
    # template_name = 'users/profile_details.html'
    model = request.user
    current_user = request.user
    context = {
        'projects': Project.objects.filter(contributors = current_user),
        'organizations': Organization.objects.filter(members = current_user),
        'lastCommit': Commit.objects.filter(author = current_user).latest('datetime'),
        'commits': Commit.objects.filter(author = current_user)
    }
    return render(request, 'users/profile_details.html', context)
