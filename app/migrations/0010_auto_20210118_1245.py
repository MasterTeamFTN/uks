# Generated by Django 3.1.5 on 2021-01-18 11:45

import app.tasks.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_taskversion_taskstate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskversion',
            name='taskState',
            field=models.CharField(blank=True, choices=[app.tasks.models.TaskState['TO_DO'], app.tasks.models.TaskState['IN_PROGRESS'], app.tasks.models.TaskState['REVIEW'], app.tasks.models.TaskState['DONE']], default='To do', max_length=255, null=True),
        ),
    ]