# Generated by Django 5.1.7 on 2025-05-26 16:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_task_description_alter_task_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='myapp.project'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='datecompleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
