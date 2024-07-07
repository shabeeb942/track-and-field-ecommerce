# Generated by Django 5.0.3 on 2024-06-08 08:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, verbose_name='Mark as Active')),
                ('image', models.ImageField(upload_to='banner')),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)s_creator', to=settings.AUTH_USER_MODEL)),
                ('sub_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.subcategory')),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CategoryOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='offers')),
                ('is_active', models.BooleanField(default=True)),
                ('is_top_selling', models.BooleanField(default=False)),
                ('is_popular', models.BooleanField(default=False)),
                ('is_new_arrival', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category')),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)s_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, verbose_name='Mark as Active')),
                ('price', models.FloatField(default=0)),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)s_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
    ]