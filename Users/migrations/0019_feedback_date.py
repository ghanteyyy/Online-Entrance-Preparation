# Generated by Django 4.2.3 on 2023-08-03 14:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0018_rename_results_exams_alter_exams_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='Date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]