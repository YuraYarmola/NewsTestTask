# Generated by Django 5.0.6 on 2024-06-01 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='sentiment',
            field=models.FloatField(null=True),
        ),
    ]
