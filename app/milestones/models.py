from django.db import models
from django.utils import timezone
from ..projects.models import Project
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django_currentuser.middleware import get_current_authenticated_user

class Milestone(models.Model):
    title = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    due_date = models.DateTimeField(null = True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('milestone-detail', kwargs={
            'project_pk': self.project.pk,
            'pk': self.pk
        })

    def save(self, *args, **kwargs):
        super(Milestone, self).save(*args, **kwargs)
