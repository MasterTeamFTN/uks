from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django_currentuser.middleware import get_current_authenticated_user

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organization-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Organization, self).save(*args, **kwargs)
        self.members.add(get_current_authenticated_user())
        super(Organization, self).save(*args, **kwargs)
