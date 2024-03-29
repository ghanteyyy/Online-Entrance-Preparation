# Generated by Django 4.1.5 on 2023-06-27 04:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0011_subject_totalquestionstoselect'),
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('ID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ProgrammeName', models.CharField(max_length=10)),
                ('CorrectCounter', models.SmallIntegerField(default=0)),
                ('Date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Results',
            },
        ),
        migrations.CreateModel(
            name='ResultDetails',
            fields=[
                ('ID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('UserAnswer', models.CharField(max_length=20)),
                ('QuestionID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.questions')),
                ('ResultID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.results')),
            ],
            options={
                'verbose_name_plural': 'ResultDetails',
            },
        ),
    ]
