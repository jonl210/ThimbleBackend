# Generated by Django 3.0.3 on 2020-07-01 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='link',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='posts.LinkMedia'),
        ),
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='posts.PhotoMedia'),
        ),
    ]