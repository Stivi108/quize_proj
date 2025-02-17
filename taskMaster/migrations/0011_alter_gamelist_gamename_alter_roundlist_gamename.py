# Generated by Django 5.0.7 on 2024-08-05 10:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskMaster', '0010_alter_roundlist_gamename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamelist',
            name='gameNAME',
            field=models.CharField(max_length=42, unique=True),
        ),
        migrations.AlterField(
            model_name='roundlist',
            name='gameName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskMaster.gamelist'),
        ),
    ]
