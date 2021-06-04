# Generated by Django 3.2.2 on 2021-06-04 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('statuses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='statuses', to='users.usermodel'),
        ),
    ]
