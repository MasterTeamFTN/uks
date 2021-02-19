from django.forms import ModelForm
from .models import Task
from ..labels.models import Label
from ..milestones.models import Milestone

class TaskCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project')
        super(TaskCreateForm, self).__init__(*args, **kwargs)

        self.fields['labels'].queryset = Label.objects.filter(project=project)
        self.fields['assignees'].queryset = project.contributors
        self.fields['milestone'].queryset = Milestone.objects.filter(project=project)

    class Meta:
        model = Task
        fields = ['title', 'description', 'labels', 'assignees', 'milestone']
