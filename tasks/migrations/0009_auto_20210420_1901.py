# Generated by Django 3.1.7 on 2021-04-20 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0008_auto_20210419_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, null=True, to='labels.Label', verbose_name='Labels'),
        ),
    ]