# Generated by Django 4.1.7 on 2023-03-10 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0002_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
