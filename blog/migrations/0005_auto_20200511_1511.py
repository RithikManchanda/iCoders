# Generated by Django 3.0.4 on 2020-05-11 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200405_1837'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-timestamp', '-updated'], 'verbose_name': 'Post'},
        ),
    ]
