# Generated by Django 4.2.15 on 2024-08-25 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskMaster', '0017_alter_gamelist_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamlist',
            name='is_ready',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
