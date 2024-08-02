
from .models import Post, Category, Comment
from django import forms


class AddCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        # widgets = {


        #     'author': forms.HiddenInput(),
        #     'created_at': forms.SplitHiddenDateTimeWidget(),
        #     'post': forms.HiddenInput()}


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('comments',)
        widgets = {
            'author': forms.HiddenInput(),
            'is_published': forms.HiddenInput(),
        }

class PostDetailForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'location', 'category', 'image',)


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'
