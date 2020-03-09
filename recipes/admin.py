from django.contrib import admin
from .models import Recipe, Category, RecipeRating

admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(RecipeRating)