# Generated by Django 4.2.1 on 2024-06-11 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encyclopedia', '0021_alter_entry_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='category',
            field=models.CharField(choices=[('people & organization', 'People & Organization'), ('person', 'Person'), ('event', 'Event'), ('entertainment', 'Entertainment'), ('place & geography', 'Place & Geography'), ('technology & innovation', 'Technology & Innovation'), ('religion & culture', 'Religion & Culture'), ('food & agriculture', 'Food & Agriculture'), ('name', 'Name'), ('language', 'Language'), ('education', 'Education')], max_length=50),
        ),
    ]