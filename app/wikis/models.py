from django.db import models
from django.utils import timezone
from ..projects.models import Project
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django_currentuser.middleware import get_current_authenticated_user

class Wiki(models.Model):
    title = models.CharField(max_length=100)
    created_on = models.DateTimeField(default=timezone.now)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    text = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('wiki-detail', kwargs={
            'project_pk': self.project.pk,
            'pk': self.pk
        })

    def save(self, *args, **kwargs):
        super(Wiki, self).save(*args, **kwargs)
        WikiVersion.objects.create(wiki=self, updated_by=get_current_authenticated_user())

class WikiVersion(models.Model):
    wiki = models.ForeignKey(Wiki, on_delete=models.CASCADE, default=None)
    updated_on = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
