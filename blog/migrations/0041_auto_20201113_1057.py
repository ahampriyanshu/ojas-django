# Generated by Django 3.0.5 on 2020-11-13 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0040_auto_20201113_1054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='unique_visitors',
            new_name='unique_visitor',
        ),
        migrations.RemoveField(
            model_name='viewer',
            name='date_last_visited',
        ),
        migrations.RemoveField(
            model_name='viewer',
            name='ip_address',
        ),
        migrations.RemoveField(
            model_name='viewer',
            name='post',
        ),
        migrations.AlterField(
            model_name='viewer',
            name='viewer',
            field=models.TextField(default=None),
        ),
    ]