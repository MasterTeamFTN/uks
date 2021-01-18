from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    github_url = models.CharField(max_length=512, default='')
    updated_on = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=True)
    contributors = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})
