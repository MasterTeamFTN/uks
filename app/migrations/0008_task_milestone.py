# Generated by Django 3.1.5 on 2021-01-17 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_task_taskversion'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='milestone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.milestone'),
        ),
    ]