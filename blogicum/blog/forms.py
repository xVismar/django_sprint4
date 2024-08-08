from django import forms

from .models import Comment, Post


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = (
            'author',
        )

        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            )}


class CreateCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
