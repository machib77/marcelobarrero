# Generated by Django 5.0.2 on 2024-05-03 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_optimization', '0002_alter_ticker_id_selectedticker'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateRange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('session_key', models.CharField(blank=True, max_length=40, null=True)),
            ],
        ),
    ]
