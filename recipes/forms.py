from django import forms

from .models import RecipeComment


class RecipeCommentForm(forms.ModelForm):
    class Meta:
        model = RecipeComment
        fields = ['created_by', 'recipe', 'text']

        widgets = {'created_by': forms.HiddenInput(), 'recipe': forms.HiddenInput(),
                   'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter Comment'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = ''
