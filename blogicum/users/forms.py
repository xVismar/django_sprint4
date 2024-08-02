from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django import forms


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'username')
        # widgets = {
        #     'some_other_field': forms.HiddenInput(),
        #     'some_other_field2': forms.DateInput(attrs={'readonly': True}),
        # }


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'username')
        exclude = ('password',)