# Generated by Django 2.2.3 on 2019-07-28 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_recipecomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipecomment',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
