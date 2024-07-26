from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .validators import real_age

from .models import Post, Category, Commentary


class CommentForm(forms.ModelForm):

    class Meta:
        model = Commentary


class PostForm(forms.ModelForm):

    class Meta:
        model = Post

    def clean(self):
        pass
        # super().clean()
        # title = self.cleaned_data['title']
        # last_name = self.cleaned_data['last_name']
        # if f'{first_name} {last_name}' in BEATLES:
        #     send_mail(
        #         subject='Another Beatles member',
        #         message=f'{first_name} {last_name} пытался опубликовать запись!',
        #         from_email='birthday_form@acme.not',
        #         recipient_list=['admin@acme.not'],
        #         fail_silently=True,
        #     )

        #     raise ValidationError(
        #         'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
        #     )


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category