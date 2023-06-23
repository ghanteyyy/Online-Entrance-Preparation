# Generated by Django 4.1.5 on 2023-06-20 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0006_programme_alter_customuser_id_subject_questions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questions',
            options={'verbose_name_plural': 'Questions'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.UUIDField(default='aa88a67b9d804ca28f216e4ea4f6b786', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='programme',
            name='ID',
            field=models.UUIDField(default='604ebc1b194a464da8e47b8b197aff10', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='questions',
            name='ID',
            field=models.UUIDField(default='039d113b6c7c4ec7962f190e3509edad', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subject',
            name='ID',
            field=models.UUIDField(default='8031eb53cb4347878844daffb8eb2163', editable=False, primary_key=True, serialize=False),
        ),
    ]