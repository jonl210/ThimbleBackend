# Generated by Django 3.0.7 on 2020-12-18 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0010_group_post_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='post_count',
        ),
    ]
