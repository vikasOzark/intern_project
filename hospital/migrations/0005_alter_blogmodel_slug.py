# Generated by Django 4.0.4 on 2022-08-21 04:01

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0004_alter_blogmodel_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogmodel',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=200, populate_from='title', unique=True),
        ),
    ]
