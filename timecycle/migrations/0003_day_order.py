# Generated by Django 5.1.3 on 2024-12-15 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timecycle', '0002_day_remove_activity_time_cycle_activity_meta_cycle_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='order',
            field=models.IntegerField(null=True),
        ),
    ]
