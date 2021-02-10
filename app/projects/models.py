from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ..organizations.models import Organization

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    github_url = models.CharField(max_length=512, default='')
    updated_on = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=True)
    contributors = models.ManyToManyField(User)
    organization = models.ForeignKey(Organization, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})

class Branch(models.Model):
    name = models.CharField(max_length=255)
    last_commit_sha = models.CharField(max_length=40)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str_(self):
        return f'{self.project.name} - {self.name}'

class Commit(models.Model):
    sha = models.CharField(max_length=40)
    message = models.CharField(max_length=500)
    github_diff_url = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    datetime = models.DateTimeField()

    # NOTE: ovde bas i nije najpametnije da stoji CASCADE, ali s obzirom
    # da nemamo brisanje korisnika, nece skoditi :D
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.sha
