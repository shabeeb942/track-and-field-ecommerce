# Generated by Django 5.0.3 on 2024-06-22 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_dealoftheday_options_productimage_color_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='color',
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(help_text=' The recommended size is 800x600 pixels.', upload_to='products/'),
        ),
    ]
