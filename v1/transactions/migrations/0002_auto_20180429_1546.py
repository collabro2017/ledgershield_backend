# Generated by Django 2.0.2 on 2018-04-29 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='destination_tag',
            field=models.CharField(blank=True, default=0, max_length=255, null=True),
        ),
    ]