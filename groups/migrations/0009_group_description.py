# Generated by Django 3.0.7 on 2020-12-11 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0008_auto_20201113_0305'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='description',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]