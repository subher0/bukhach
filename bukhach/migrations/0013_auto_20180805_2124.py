# Generated by Django 2.0.1 on 2018-08-05 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bukhach', '0012_auto_20180805_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinterval',
            name='gathering_id',
        ),
        migrations.AddField(
            model_name='userinterval',
            name='gathering',
            field=models.ForeignKey(blank=True, db_column='gathering_id', default=None, on_delete=django.db.models.deletion.CASCADE, to='bukhach.Gathering', verbose_name='Gathering'),
        ),
    ]