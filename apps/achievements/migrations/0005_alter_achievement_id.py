# Generated by Django 4.2.16 on 2024-10-28 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0004_auto_20210730_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
