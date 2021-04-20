# Generated by Django 3.1.7 on 2021-04-10 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0003_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='label',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='labels.label'),
        ),
    ]