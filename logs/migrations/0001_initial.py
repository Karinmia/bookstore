# Generated by Django 2.1.7 on 2019-03-11 11:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CRUDLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('isbn', models.CharField(max_length=18)),
                ('request_type', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='HttpLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('isbn', models.CharField(max_length=18)),
                ('request_type', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
