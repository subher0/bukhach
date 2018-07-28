# Generated by Django 2.0.1 on 2018-07-28 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bukhach', '0008_auto_20180409_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='gathering',
            name='name',
            field=models.CharField(default='Gay gathering', max_length=64, verbose_name='Gathering name'),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_ip',
            field=models.CharField(blank=True, default=None, max_length=16, null=True, verbose_name='Last IP adress'),
        ),
        migrations.AlterField(
            model_name='gathering',
            name='gathering_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='YourGatherings', to='bukhach.Profile', verbose_name='Gathering creator'),
        ),
        migrations.AlterField(
            model_name='gathering',
            name='users',
            field=models.ManyToManyField(related_name='gatherings', to='bukhach.Profile', verbose_name='Users'),
        ),
        migrations.AlterField(
            model_name='gatheringapplication',
            name='applicant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bukhach.Profile', verbose_name='Applicant'),
        ),
        migrations.AlterField(
            model_name='gatheringapplication',
            name='gathering',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='bukhach.Gathering', verbose_name='Gathering'),
        ),
        migrations.AlterField(
            model_name='gatheringinterval',
            name='gathering',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='interval', to='bukhach.Gathering', verbose_name='Gathering'),
        ),
        migrations.AlterField(
            model_name='userinterval',
            name='gathering_id',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='bukhach.Gathering', verbose_name='Gathering'),
        ),
        migrations.AlterField(
            model_name='userinterval',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bukhach.Profile', verbose_name='User'),
        ),
    ]
