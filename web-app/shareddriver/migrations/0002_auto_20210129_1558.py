# Generated by Django 3.1.5 on 2021-01-29 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shareddriver', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicle', to='shareddriver.user'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ride', to='shareddriver.user'),
        ),
    ]