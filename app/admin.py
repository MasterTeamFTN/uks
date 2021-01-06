from django.contrib import admin
from .models import Project, Wiki, WikiVersion

admin.site.register(Project)
admin.site.register(Wiki)
admin.site.register(WikiVersion)
