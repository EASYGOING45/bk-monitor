# Generated by Django 3.2.15 on 2024-12-04 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bkmonitor', '0166_auto_20241112_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='shield',
            name='label',
            field=models.CharField(blank=True, db_index=True, default='', max_length=32, verbose_name='标签'),
        ),
    ]