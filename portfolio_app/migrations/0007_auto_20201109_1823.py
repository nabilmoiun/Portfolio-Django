# Generated by Django 3.0.7 on 2020-11-09 12:23

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_app', '0006_auto_20201109_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='work_description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='joined',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
