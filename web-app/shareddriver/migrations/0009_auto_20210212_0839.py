# Generated by Django 3.1.5 on 2021-02-12 08:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shareddriver', '0008_ride_editable'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='date',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='time',
        ),
        migrations.AddField(
            model_name='ride',
            name='date_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]