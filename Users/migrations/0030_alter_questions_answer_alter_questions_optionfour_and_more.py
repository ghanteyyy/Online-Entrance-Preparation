# Generated by Django 5.1.6 on 2025-02-11 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0029_programme_totalquestions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='Answer',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='questions',
            name='OptionFour',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='questions',
            name='OptionOne',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='questions',
            name='OptionThree',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='questions',
            name='OptionTwo',
            field=models.TextField(),
        ),
    ]
