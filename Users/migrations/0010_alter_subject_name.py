# Generated by Django 4.1.5 on 2023-06-21 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0009_alter_customuser_id_alter_programme_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='Name',
            field=models.CharField(max_length=50),
        ),
    ]