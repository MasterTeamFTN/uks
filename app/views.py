from django.shortcuts import render
from django.urls import reverse_lazy
from app.models import Project, Wiki
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    current_user = request.user
    context = {
        'projects': Project.objects.filter(contributors = current_user.id)
    }
    print (context)
    return render(request, 'app/home.html', context)

def about(request):
    return render(request, 'app/about.html')

def projects(request):
    context = {
        'projects': Project.objects.all()
    }
    return render(request, 'app/projects.html', context);


class ProjectDetailView(DetailView):
    model = Project 

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project 
    success_url = '/'

    def test_func(self):
        project = self.get_object()
        if self.request.user.id in project.contributors.all():
            return True
        return False


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project 
    fields = ['name', 'description', 'is_public', 'contributors']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class WikiListView(ListView):
    model = Wiki
    context_object_name = 'wikis'
    ordering = ['created_on']

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)
        return Wiki.objects.filter(project=project)

def wikis_list_view(request, project_pk):
    project = Project.objects.get(pk=project_pk)
     
    context = {
        'wikis': Wiki.objects.filter(project=project),
        'project': project
    }

    return render(request, 'app/wiki_list.html', context)

class WikiDetailView(DetailView):
    model = Wiki

class WikiCreateView(LoginRequiredMixin, CreateView):
    model = Wiki
    fields = ['title', 'text']

    def form_valid(self, form):
        project_id = self.kwargs.get('project_pk')
        form.instance.project = Project.objects.get(pk=project_id)
        return super().form_valid(form)


class WikiDeleteView(LoginRequiredMixin, DeleteView):
    model = Wiki 

    def get_success_url(self):
        wiki = self.get_object() 
        return reverse_lazy('wiki-list', kwargs={'project_pk': wiki.project.id})

    def test_func(self):
        wiki = self.get_object()
        return self.request.user.id in wiki.project.contributors.all()
