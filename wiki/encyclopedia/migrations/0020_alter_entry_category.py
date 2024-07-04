# Generated by Django 4.2.1 on 2024-06-11 13:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('encyclopedia', '0019_entry_bio_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='category',
            field=models.CharField(choices=[('people_organization', 'People & Organization'), ('person', 'Person'), ('event', 'Event'), ('entertainment', 'Entertainment'), ('place_geography', 'Place & Geography'), ('technology_innovation', 'Technology & Innovation'), ('religion_culture', 'Religion & Culture'), ('food_agriculture', 'Food & Agriculture'), ('name', 'Name'), ('language', 'Language')], default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]