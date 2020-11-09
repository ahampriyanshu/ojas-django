# Generated by Django 3.0.5 on 2020-11-09 22:00

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_auto_20201110_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='joined',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 9, 22, 0, 36, 887005, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Author'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 9, 22, 0, 36, 904632, tzinfo=utc)),
        ),
    ]
