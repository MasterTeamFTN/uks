from django.contrib import admin
from .projects.models import Project
from .labels.models import Label
from .wikis.models import Wiki, WikiVersion

admin.site.register([
    Project,
    Label,
    Wiki,
    WikiVersion,
])
