# Generated by Django 5.1.3 on 2024-11-24 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CreateEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_title', models.CharField(max_length=255)),
                ('established_in', models.IntegerField()),
                ('contact', models.CharField(max_length=15)),
                ('wh_number', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=255)),
                ('services', models.TextField()),
                ('event_photos', models.ImageField(upload_to='images/')),
            ],
            options={
                'db_table': 'create_event',
            },
        ),
    ]