# Generated by Django 4.2.1 on 2024-05-03 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encyclopedia', '0009_alter_entry_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
