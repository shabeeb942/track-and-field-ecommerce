# Generated by Django 5.0.3 on 2024-06-12 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_remove_dealoftheday_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealoftheday',
            name='is_offer_end',
            field=models.BooleanField(default=False),
        ),
    ]
