# Generated by Django 5.0.7 on 2024-08-01 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskMaster', '0006_alter_teamlist_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='roundlist',
            name='target',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='teamlist',
            name='points',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
    ]
