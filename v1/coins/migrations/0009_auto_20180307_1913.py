# Generated by Django 2.0.2 on 2018-03-07 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0008_auto_20180307_1810'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coin',
            old_name='fee',
            new_name='service_fee',
        ),
        migrations.AddField(
            model_name='coin',
            name='fee_per_kb',
            field=models.PositiveIntegerField(default=0),
        ),
    ]