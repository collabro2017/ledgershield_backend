# Generated by Django 2.0.2 on 2018-02-21 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='despoit',
            new_name='deposit',
        ),
    ]
