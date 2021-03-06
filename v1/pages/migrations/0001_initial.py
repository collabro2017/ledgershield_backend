# Generated by Django 2.0.2 on 2018-04-05 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('name', models.CharField(db_index=True, max_length=50, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('content', models.TextField()),
            ],
        ),
    ]
