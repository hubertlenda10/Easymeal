from faker import Faker
from django.contrib.auth.models import User
from django.utils import timezone
from recipes.models import Category, RecipeRating, Recipe, RecipeComment
from website.models import Post, PostComment, News

fake = Faker()
users = User.objects.all()

ratings = RecipeRating.objects.all()

import random

category_names = ['breakfast', 'lunch', 'dinner']


def generate_fake_categories():
    Category.objects.all().delete()

    for name in category_names:
        print('generating categories')
        Category.objects.create(
            name=name
        )


def generate_fake_recipes():
    categories = Category.objects.all()
    Recipe.objects.all().delete()
    for i in range(10):
        print('generating recipes')
        recipe = Recipe.objects.create(
            title=fake.word(),
            content=fake.sentence(),
            date_created=timezone.now(),
            directions=fake.paragraph(),
            cooking_time=fake.sentence(),
            ingredients=fake.sentence(),
            allergens=fake.sentence(),
            created_by=random.choice([user for user in users]),
            category=random.choice([category for category in categories])
        )


def generate_fake_ratings():
    RecipeRating.objects.all().delete()
    for recipe in Recipe.objects.all():
        for user in users:
            print('generating ratings')
            RecipeRating.objects.create(
                recipe=recipe,
                created_by=user,
                rating=random.choice([_ for _ in range(1, 6)])
            )


def generate_fake_posts():
    Post.objects.all().delete()

    for i in range(10):
        print('generating posts')
        Post.objects.create(
            title=fake.sentence(),
            content=fake.paragraph(),
            created_by=random.choice(users)
        )


def generate_fake_comments():
    RecipeComment.objects.all().delete()
    PostComment.objects.all().delete()

    for recipe in Recipe.objects.all():
        for i in range(random.randint(1, 5)):
            print('generating recipe comments')
            RecipeComment.objects.create(
                text=fake.paragraph(),
                recipe=recipe,
                created_by=random.choice(users)
            )

    for post in Post.objects.all():
        for i in range(random.randint(1, 5)):
            print('generating post comments')
            PostComment.objects.create(
                text=fake.paragraph(),
                post=post,
                created_by=random.choice(users)
            )


def generate_fake_news():
    for i in range(10):
        print('generating news')
        News.objects.create(
            title=fake.sentence(),
            description=fake.paragraph(),
            created_by=random.choice(users),
            url=fake.url(),
            image_url="https://picsum.photos/500"
        )


def run():
    generate_fake_categories()
    generate_fake_recipes()
    generate_fake_ratings()
    generate_fake_posts()
    generate_fake_comments()
    generate_fake_news()
