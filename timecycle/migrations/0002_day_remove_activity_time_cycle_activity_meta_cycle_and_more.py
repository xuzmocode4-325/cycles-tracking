# Generated by Django 5.1.3 on 2024-12-15 12:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timecycle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=3)),
            ],
        ),
        migrations.RemoveField(
            model_name='activity',
            name='time_cycle',
        ),
        migrations.AddField(
            model_name='activity',
            name='meta_cycle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='timecycle.metacycle'),
        ),
        migrations.RemoveField(
            model_name='metacycle',
            name='frequency',
        ),
        migrations.DeleteModel(
            name='TimeCycle',
        ),
        migrations.AddField(
            model_name='metacycle',
            name='frequency',
            field=models.ManyToManyField(to='timecycle.day'),
        ),
    ]
