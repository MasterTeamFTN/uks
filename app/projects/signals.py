from ..utils.default_labels import default_labels
from ..utils.github_utils import get_branches_and_commits
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..labels.models import Label
from .models import Project
from django.contrib.auth.models import User
import requests

@receiver(post_save, sender=Project)
def create_default_labels(sender, instance, created, **kwargs):
    """
    Creates default labels when new project is created
    """
    if not created:
        return

    for label in default_labels:
        Label.objects.create(name=label['name'], description=label['description'], project=instance, color=label['color'])

@receiver(post_save, sender=Project)
def get_branches_from_github(sender, instance, created, **kwargs):
    """
    Get all branches from Github and save them in database
    after new project has been created
    """
    if not created:
        return

    get_branches_and_commits(instance)
