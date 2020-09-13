# Generated by Django 2.2.4 on 2020-02-06 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20191106_1917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='multiple_to_dos_choice',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='starview_multipletodos_choice',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='treeview_multipletodos_choice',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='strategy_choice',
            field=models.CharField(choices=[('ALL', 'Show all strategies.'), ('STAR', 'Show all starred strategies.'), ('NONE', 'Show no strategies.')], default='ALL', max_length=10),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='treeview_strategy_choice',
            field=models.CharField(choices=[('ALL', 'Show all strategies.'), ('STAR', 'Show all starred strategies.'), ('NONE', 'Show no strategies.')], default='ALL', max_length=10),
        ),
    ]