from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=True)
    contributors = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})

class Wiki(models.Model):
    title = models.CharField(max_length=100)
    created_on = models.DateTimeField(default=timezone.now)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # todo: dodati richtextfield

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('wiki-detail', kwargs={
            'project_pk': self.project.pk,
            'pk': self.pk
        })

class WikiVersion(models.Model):
    updated_on = models.DateTimeField(default=timezone.now)
    updated_by = models.OneToOneField(User, on_delete=models.CASCADE)
