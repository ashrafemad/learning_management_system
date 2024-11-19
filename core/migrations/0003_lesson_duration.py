# Generated by Django 5.1.3 on 2024-11-18 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_alter_lesson_course"),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="duration",
            field=models.PositiveIntegerField(
                default=1, help_text="duration in minutes"
            ),
        ),
    ]
