# Generated by Django 3.1.5 on 2021-01-18 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20210118_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskversion',
            name='task_state',
            field=models.CharField(blank=True, choices=[('TO_DO', 'To do'), ('IN_PROGRESS', 'In progress'), ('REVIEW', 'Review'), ('DONE', 'Done')], max_length=255, null=True),
        ),
    ]
