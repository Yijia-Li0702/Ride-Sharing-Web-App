# Generated by Django 3.1.5 on 2021-02-12 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareddriver', '0009_auto_20210212_0839'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='password',
            new_name='pwd',
        ),
    ]