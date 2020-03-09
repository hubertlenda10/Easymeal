from django.urls import path, include
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    PostCommentCreateView,
    PostCommentListView,
    SearchIngredients
)
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='website-home'),
    path('about/', views.about, name='website-about'),
    path('blog/', PostListView.as_view(), name='website-blog'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('blog/post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('blog/post/new/', PostCreateView.as_view(), name='post-create'),
    path('blog/post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('blog/post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('recipes/recipes_list/', views.recipes_list, name='recipes-recipes_list'),
    path('post_comments', PostCommentListView.as_view(), name='post-comments-list'),
    path('post_comment_create', PostCommentCreateView.as_view(), name='post-comment-create'),
    path('search_ingredients', SearchIngredients.as_view(), name="search-ingredients")
]
