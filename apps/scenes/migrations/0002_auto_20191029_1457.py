# Generated by Django 2.2.6 on 2019-10-29 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alarmlamp',
            old_name='scene_id',
            new_name='scene',
        ),
        migrations.RenameField(
            model_name='alertor',
            old_name='scene_id',
            new_name='scene',
        ),
        migrations.RenameField(
            model_name='beam',
            old_name='scene_id',
            new_name='scene',
        ),
        migrations.RenameField(
            model_name='co2',
            old_name='scene_id',
            new_name='scene',
        ),
        migrations.RenameField(
            model_name='display',
            old_name='scene_id',
            new_name='scene',
        ),
        migrations.RenameField(
            model_name='fan',
            old_name='scene_id',
            new_name='scene',
        ),
        migrations.RenameField(
            model_name='flame',
            old_name='scene_id',
            new_name='scene',
        ),
        migrations.RenameField(
            model_name='humidity',
            old_name='scene_id',
            new_name='scene',
        ),
        migrations.RenameField(
            model_name='invade',
            old_name='scene_id',
            new_name='scene',
        ),
        migrations.RenameField(
            model_name='light',
            old_name='scene_id',
            new_name='scene',
        ),
        migrations.RenameField(
            model_name='methane',
            old_name='scene_id',
            new_name='scene',
        ),
        migrations.RenameField(
            model_name='pm25',
            old_name='scene_id',
            new_name='scene',
        ),
        migrations.RenameField(
            model_name='pump',
            old_name='scene_id',
            new_name='scene',
        ),
        migrations.RenameField(
            model_name='smoke',
            old_name='scene_id',
            new_name='scene',
        ),
        migrations.RenameField(
            model_name='temperature',
            old_name='scene_id',
            new_name='scene',
        ),
        migrations.RenameField(
            model_name='unlocking',
            old_name='scene_id',
            new_name='scene',
        ),
        migrations.AddField(
            model_name='scene',
            name='scene_gateway',
            field=models.CharField(max_length=255, null=True, verbose_name='网关密码'),
        ),
    ]
