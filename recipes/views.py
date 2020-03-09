from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.views import View
from django.template.loader import render_to_string
from .models import Recipe, Category, RecipeRating, RecipeComment
from .forms import RecipeCommentForm
from django.db.models import Avg

from el_pagination.views import AjaxListView


def recipes_list(request):
    context = {

        'recipes': Recipe.objects.all()
    }
    return render(request, 'recipes/recipes_list.html', context, {'title': 'Recipes'})


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'
    context_object_name = 'recipes'
    ordering = ['-date_created']
    paginate_by = 12

    def get_queryset(self):
        category = self.request.GET.get('category', None)
        queryset = Recipe.objects.order_by('-date_created')

        if category:
            queryset = queryset.filter(category__id=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category')
        context['current_category'] = ''

        if category and category.isdigit():
            current_category = Category.objects.filter(id=int(category))

            if current_category.exists():
                context['current_category'] = current_category.first().name.capitalize()

        return context


class UserRecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/user_recipes.html'
    context_object_name = 'recipes'
    paginate_by = 12

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Recipe.objects.filter(created_by=user).order_by('-date_created')


class RecipeDetailView(DetailView):
    model = Recipe


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['title', 'content', 'category', 'directions', 'ingredients', 'cooking_time', 'allergens', 'image']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    fields = ['title', 'content', 'directions', 'ingredients', 'cooking_time', 'allergens', 'image']
    success_url = '/recipes'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.created_by:
            return True
        return False


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = '/recipes'

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.created_by:
            return True
        return False


class RecipeRatingCreateView(View):

    def post(self, request):
        recipe_id = request.POST.get('recipe_id', None)
        rating = request.POST.get('rating', None)

        if recipe_id and rating:
            recipe = Recipe.objects.filter(id=recipe_id)

            if recipe.exists():
                recipe = recipe.first()
                recipe_rating, _ = RecipeRating.objects.get_or_create(
                    created_by=request.user,
                    recipe=recipe
                )

                recipe_rating.rating = rating
                recipe_rating.save()

                average_rating = recipe.ratings.aggregate(average_rating=Avg('rating'))['average_rating']

                return JsonResponse(dict(
                    rating=rating,
                    rating_info=f'&emsp; average rating: {round(average_rating, 2)}',
                    success=True,
                    message='Thanks for your rating'
                ))

        return JsonResponse(dict(success=False, message="Something went wrong"))


class RecipeCommentListView(AjaxListView):
    model = RecipeComment
    template_name = "core/comments.html"
    page_template = "core/comment_page.html"
    context_object_name = "comments"

    def get_queryset(self):
        recipe_id = self.request.GET.get('recipe_id', None)
        recipe_comments = RecipeComment.objects.order_by('date_created')

        if recipe_id:
            recipe_comments = recipe_comments.filter(recipe_id=recipe_id)

        return recipe_comments


class RecipeCommentCreateView(CreateView):
    model = RecipeComment
    form_class = RecipeCommentForm
    template_name = 'recipes/recipe_comment_form.html'

    def form_valid(self, form):
        comment = form.save()
        return JsonResponse(dict(
            success=True,
            message="Recipe comment added successfully",
            html=render_to_string('core/comment_card.html', context=dict(comment=comment)),
            comments_count=comment.recipe.comments.count()
        ))

    def form_invalid(self, form):
        return JsonResponse(
            dict(
                success=False,
                errors=form.errors.as_json()
            )
        )
