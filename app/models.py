from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from colorfield.fields import ColorField
from ckeditor.fields import RichTextField
from django_currentuser.middleware import get_current_authenticated_user

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

class Label(models.Model):
    name = models.CharField(max_length=100)
    color = ColorField(default='#FF0000')
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('app-labels')

class Dummy(models.Model):
    name = models.CharField(max_length=100)
    dummyField = models.CharField(max_length=44)

class Wiki(models.Model):
    dummyField = models.CharField(max_length=41)
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
        is_new = True if not self.id else False
        super(Wiki, self).save(*args, **kwargs)
        WikiVersion.objects.create(wiki=self, updated_by=get_current_authenticated_user())


class WikiVersion(models.Model):
    wiki = models.ForeignKey(Wiki, on_delete=models.CASCADE, default=None)
    updated_on = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
