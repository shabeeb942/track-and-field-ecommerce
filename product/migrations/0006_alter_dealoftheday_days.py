# Generated by Django 5.0.3 on 2024-06-11 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_dealoftheday_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealoftheday',
            name='days',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
