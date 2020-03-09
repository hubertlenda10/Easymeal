from django.urls import path, include
from .views import (
    RecipeListView,
    RecipeDetailView,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
    UserRecipeListView,
    RecipeRatingCreateView,
    RecipeCommentListView,
    RecipeCommentCreateView
)

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipes-recipes_list'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('user/<str:username>/', UserRecipeListView.as_view(), name='user-recipes'),
    path('recipe/new/', RecipeCreateView.as_view(), name='recipe-create'),
    path('recipe/<int:pk>/update/', RecipeUpdateView.as_view(), name='recipe-update'),
    path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe-delete'),
    path('recipe_rating_create', RecipeRatingCreateView.as_view(), name='recipe-rating-create'),
    path('recipe_comments', RecipeCommentListView.as_view(), name='recipe-comments-list'),
    path('recipe_comment_create', RecipeCommentCreateView.as_view(), name='recipe-comment-create')
]
