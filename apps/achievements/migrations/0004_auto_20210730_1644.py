# Generated by Django 2.2.16 on 2021-07-30 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("achievements", "0003_auto_20210730_1641"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="achievement",
            options={
                "ordering": ["-date"],
                "verbose_name": "Achievement",
                "verbose_name_plural": "Achievements",
            },
        ),
    ]
