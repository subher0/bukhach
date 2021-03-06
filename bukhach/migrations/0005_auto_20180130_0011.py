# Generated by Django 2.0.1 on 2018-01-29 21:11

import bukhach.models.profile_models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bukhach', '0004_auto_20180124_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='tel_num',
            field=models.CharField(blank=True, max_length=11, verbose_name='tel_num'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='def_ava.png', upload_to=bukhach.models.profile_models.make_filepath, verbose_name='avatar'),
        ),
    ]
