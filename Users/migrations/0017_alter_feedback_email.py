# Generated by Django 4.2.2 on 2023-07-19 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0016_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='Email',
            field=models.EmailField(max_length=254),
        ),
    ]
