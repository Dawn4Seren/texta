# Generated by Django 2.0.2 on 2019-01-23 14:21

from django.db import migrations, models
import uuid

def combine_names(apps, schema_editor):
    
    Task = apps.get_model('task_manager', 'Task')
    for i, task in enumerate(Task.objects.all()):
        newuuid = uuid.uuid4()
        print(newuuid)
        task.unique_id = newuuid#newid
        task.save()


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0002_auto_20190123_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),

        migrations.RunPython(combine_names),

        migrations.AlterField(
            model_name='task',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]