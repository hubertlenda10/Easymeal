from django import forms

from .models import PostComment


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['created_by', 'post', 'text']

        widgets = {'created_by': forms.HiddenInput(), 'post': forms.HiddenInput(),
                   'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter Comment'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = ''
