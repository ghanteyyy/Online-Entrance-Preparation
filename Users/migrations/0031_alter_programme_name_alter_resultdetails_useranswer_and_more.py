# Generated by Django 5.1.7 on 2025-03-29 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0030_alter_questions_answer_alter_questions_optionfour_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programme',
            name='Name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='resultdetails',
            name='UserAnswer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='subject',
            name='Name',
            field=models.CharField(max_length=255),
        ),
    ]
