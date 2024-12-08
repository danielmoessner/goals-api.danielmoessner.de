# Generated by Django 4.2.16 on 2024-11-11 00:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notes", "0005_alter_note_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="note",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="note",
            name="updated",
            field=models.DateTimeField(
                auto_now=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
