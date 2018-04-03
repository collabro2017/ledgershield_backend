# Generated by Django 2.0.2 on 2018-04-03 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0022_auto_20180403_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('submitted', 'Submitted'), ('awaiting', 'Waiting for deposit'), ('deposit_received', 'Deposit received'), ('waiting_for_confirmation', 'Waiting for confirmation'), ('exchange', 'Exchanging'), ('out_order', 'Out of order'), ('completed', 'Completed'), ('refunded', 'Refunded'), ('partial_filled', 'Partially Filled')], db_index=True, default='submitted', max_length=100),
        ),
    ]