# Generated by Django 3.0.4 on 2020-04-05 13:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200405_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='published',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
