# Generated by Django 4.2.1 on 2024-06-11 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encyclopedia', '0023_alter_entry_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='entry',
            name='tag',
        ),
        migrations.AddField(
            model_name='entry',
            name='tag',
            field=models.ManyToManyField(blank=True, to='encyclopedia.tag'),
        ),
    ]