# Generated by Django 4.2.1 on 2024-04-30 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encyclopedia', '0006_entry'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='category',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='entry',
            name='reference',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='tag',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
