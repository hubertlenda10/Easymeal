from django import template

from recipes.models import RecipeRating

register = template.Library()


@register.simple_tag
def get_rating(user, recipe):
    recipe_rating = RecipeRating.objects.filter(created_by=user, recipe=recipe)

    if recipe_rating.exists():
        return recipe_rating.first().rating

    else:
        return 0

