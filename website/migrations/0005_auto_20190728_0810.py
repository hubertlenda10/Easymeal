# Generated by Django 2.2.3 on 2019-07-28 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20190728_0806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='date_posted',
        ),
        migrations.AddField(
            model_name='post',
            name='date_created',
            field=models.DateTimeField(null=True),
        ),
    ]
