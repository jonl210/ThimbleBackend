# Generated by Django 3.0.7 on 2020-12-18 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0009_group_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='post_count',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]