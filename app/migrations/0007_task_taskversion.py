# Generated by Django 3.1.5 on 2021-01-17 19:04

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0006_auto_20210113_2106'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('assignees', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('labels', models.ManyToManyField(to='app.Label')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.project')),
            ],
        ),
        migrations.CreateModel(
            name='TaskVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('task', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.task')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
