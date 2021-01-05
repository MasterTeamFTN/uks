from django.contrib import admin
from .models import Project, Label, Wiki, WikiVersion

admin.site.register(Project)
admin.site.register(Label)
admin.site.register(Wiki)
admin.site.register(WikiVersion)
