# Generated by Django 3.0.5 on 2020-11-22 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20201122_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='default_page',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default='Yes'),
        ),
    ]
