from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from ..projects.models import Project
from ..labels.models import Label
from ..milestones.models import Milestone
from django_currentuser.middleware import get_current_authenticated_user
from django.utils.translation import gettext_lazy as _

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=True)
    assignees = models.ManyToManyField(User)
    labels = models.ManyToManyField(Label)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})
    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)
        TaskVersion.objects.create(task=self, updated_by=get_current_authenticated_user(), task_state=TaskState.TO_DO)

class TaskState(models.TextChoices):
    TO_DO = 'TO_DO', _('To do')
    IN_PROGRESS = 'IN_PROGRESS', _('In progress')
    REVIEW = 'REVIEW', _('Review')
    DONE = 'DONE', _('Done')

class TaskVersion(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, default=None)
    updated_on = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)

    task_state = models.CharField(
        max_length=255,
        choices=TaskState.choices,
        blank=True, null=True
    )
