# Generated by Django 5.1.6 on 2025-04-26 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_rename_text_tip_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='daily_steps_goal',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='daily_water_goal',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='weekly_activity_goal',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='weight_goal',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
