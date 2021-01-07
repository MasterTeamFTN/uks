from django.db import models
from django.urls import reverse
from ..projects.models import Project
from colorfield.fields import ColorField

class Label(models.Model):
    name = models.CharField(max_length=100)
    color = ColorField(default='#FF0000')
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('label-list', kwargs={
            'project_pk': self.project.pk
        })
