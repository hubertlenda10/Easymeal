# Generated by Django 2.2.3 on 2019-08-01 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_auto_20190731_1653'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='total_rating',
            new_name='average_rating',
        ),
    ]
