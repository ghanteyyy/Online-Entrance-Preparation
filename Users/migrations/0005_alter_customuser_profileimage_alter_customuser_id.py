# Generated by Django 4.1.5 on 2023-06-17 09:20

import Users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_alter_customuser_profileimage_alter_customuser_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='ProfileImage',
            field=models.ImageField(blank=True, default='pp-female.jpg', null=True, upload_to=Users.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.UUIDField(default='a2d2af8fb8ac4aed9ae22616a8befb4e', editable=False, primary_key=True, serialize=False),
        ),
    ]