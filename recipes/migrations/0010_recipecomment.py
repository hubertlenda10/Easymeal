# Generated by Django 2.2.3 on 2019-07-28 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20190727_1907'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('date_created', models.DateTimeField(null=True)),
                ('approved_comment', models.BooleanField(default=False)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='recipes.Recipe')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
