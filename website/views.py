from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models.aggregates import Count
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.views import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Post, PostComment, News
from .forms import PostCommentForm
from recipes.models import Category, Recipe
from el_pagination.views import AjaxListView


class HomeView(View):

    def get(self, request):
        context = dict()
        recipes = Recipe.objects.order_by('-average_rating')
        categories = Category.objects.order_by('-id')
        context['categories'] = categories
        context['recipes'] = dict()

        for category in categories:
            context['recipes'][category.name] = recipes.filter(average_rating__gt=0).filter(category=category)[:3]

        context['highest_recipe_count_users'] = User.objects.filter(recipes__isnull=False).annotate(
            recipe_count=Count('recipes__id')
        ).order_by('-recipe_count')[:5]

        return render(request, 'website/home.html', context)


class SearchIngredients(View):

    def get(self, request):
        recipes = None
        search_query = request.GET.get('query', None)
        context = dict()

        if search_query:
            recipes = Recipe.objects.filter(ingredients__icontains=search_query)

        context['recipes'] = recipes
        context['request'] = request
        return JsonResponse(dict(html=render_to_string('website/searched_recipes.html', context)))


def about(request):
    return render(request, 'website/about.html', {'title': 'About'})


def blog(request):
    context = {

        'posts': Post.objects.all()
    }
    return render(request, 'website/blog.html', context, {'title': 'Healthy Blog'})


class UserPostListView(ListView):
    model = Post
    template_name = 'website/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_created']
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(created_by=user).order_by('-date_created')


class PostListView(ListView):
    model = Post
    template_name = 'website/blog.html'
    context_object_name = 'posts'
    ordering = ['-date_created']
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_news'] = News.objects.order_by('-id')[:5]

        return context


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        print(self.request.FILES)
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.created_by:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.created_by:
            return True
        return False


def recipes_list(request):
    return render(request, 'recipes/recipes_list.html', {'title': 'Recipes'})


class PostCommentListView(AjaxListView):
    model = PostComment
    template_name = "core/comments.html"
    page_template = "core/comment_page.html"
    context_object_name = "comments"

    def get_queryset(self):
        post_id = self.request.GET.get('post_id', None)
        post_comments = PostComment.objects.order_by('date_created')

        if post_id:
            post_comments = post_comments.filter(post_id=post_id)

        return post_comments


class PostCommentCreateView(CreateView):
    model = PostComment
    form_class = PostCommentForm
    template_name = 'website/post_comment_form.html'

    def form_valid(self, form):
        comment = form.save()
        return JsonResponse(dict(
            success=True,
            message="Post comment added successfully",
            html=render_to_string('core/comment_card.html', context=dict(comment=comment)),
            comments_count=comment.post.comments.count()
        ))

    def form_invalid(self, form):
        return JsonResponse(
            dict(
                success=False,
                errors=form.errors.as_json()
            )
        )
