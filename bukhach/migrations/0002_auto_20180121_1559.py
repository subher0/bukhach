# Generated by Django 2.0.1 on 2018-01-21 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bukhach', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinterval',
            old_name='endDate',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='userinterval',
            old_name='startDate',
            new_name='start_date',
        ),
    ]
