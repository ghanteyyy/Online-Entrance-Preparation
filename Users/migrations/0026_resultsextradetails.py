# Generated by Django 4.2.3 on 2023-12-04 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0025_customuser_teststaken_alter_customuser_profileimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultsExtraDetails',
            fields=[
                ('ID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'ResultsExtraDetails',
            },
        ),
    ]
