# Generated by Django 3.1.5 on 2021-01-06 21:27

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_label_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', max_length=18),
        ),
    ]