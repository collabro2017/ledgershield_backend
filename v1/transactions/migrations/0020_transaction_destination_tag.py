# Generated by Django 2.0.2 on 2018-04-02 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0019_auto_20180328_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='destination_tag',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
