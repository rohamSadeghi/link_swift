# Generated by Django 4.2.4 on 2023-08-27 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShortenedURL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True)),
                ('short_code', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('hits', models.PositiveIntegerField(default=0)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
    ]
