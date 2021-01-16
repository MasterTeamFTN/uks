from ..utils.default_labels import default_labels
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..labels.models import Label
from .models import Project

@receiver(post_save, sender=Project)
def create_default_labels(sender, instance, created, **kwargs):
    """
    Creates default labels when new project is created
    """
    if not created:
        return

    for label in default_labels:
        Label.objects.create(name=label['name'], description=label['description'], project=instance, color=label['color'])
