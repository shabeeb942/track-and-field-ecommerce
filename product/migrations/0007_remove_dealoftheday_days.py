# Generated by Django 5.0.3 on 2024-06-11 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_dealoftheday_days'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dealoftheday',
            name='days',
        ),
    ]
