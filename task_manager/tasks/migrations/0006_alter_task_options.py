# Generated by Django 5.0.6 on 2024-07-19 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0005_alter_task_author_alter_task_executor"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="task",
            options={
                "permissions": [
                    ("tasks.delete_all", "Can delete all tasks"),
                    ("tasks.delete_own", "Can delete own tasks"),
                ]
            },
        ),
    ]
