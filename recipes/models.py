from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Avg
from django.db.models.signals import post_save
from core.models import Comment


class Category(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='category_recipe_pics', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(null=True)
    image = models.ImageField(null=True, blank=True, upload_to='recipe_pics')
    directions = models.TextField()
    cooking_time = models.TextField()
    ingredients = models.TextField()
    allergens = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    category = models.ForeignKey(Category, related_name='recipes', on_delete=models.CASCADE)
    average_rating = models.FloatField(default=0, blank=True)

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        if not self.date_created:
            self.date_created = timezone.now()

        return super().save(**kwargs)

    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'pk': self.pk})

    @property
    def rating_count(self):
        return self.ratings.count()


class RecipeRating(models.Model):
    created_by = models.ForeignKey(User, related_name='recipe_ratings', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='ratings', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    date_created = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = 'Recipe Ratings'
        unique_together = ('recipe', 'created_by')

    def save(self, **kwargs):
        if not self.date_created:
            self.date_created = timezone.now()

        super().save(**kwargs)


class RecipeComment(Comment):
    created_by = models.ForeignKey(User, related_name='recipe_comments', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE)


def recipe_rating_update(sender, instance, created, **kwargs):
    recipe = instance.recipe
    average_rating = recipe.ratings.aggregate(average_rating=Avg('rating'))['average_rating']
    recipe.average_rating = round(average_rating, 2)
    recipe.save()


post_save.connect(recipe_rating_update, sender=RecipeRating)

