# Generated by Django 3.0.3 on 2020-03-08 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_auto_20200308_0432'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='banner',
            field=models.URLField(default='replace'),
        ),
    ]
