from calendar import c
from webbrowser import get
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from blog.models import Post, Comment
from blog.forms import CreatePostForm, AddCommentForm
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render
from users.forms import ProfileForm, EditProfileForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic.list import MultipleObjectMixin
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
from django.contrib.auth import authenticate



DISP_LIMIT = 10


# class UserRegistView(CreateView):
#     template_name = 'registration/registration_form.html'
#     form_class = UserCreationForm
#     success_url = reverse_lazy('blog:index')

def registration(request):
    template = 'registration/registration_form.html'
    form = UserCreationForm(request.POST or None)
    context = {'form': form}

    if form.is_valid():
        form.save()
        user = authenticate(request, username=f"{form.cleaned_data.get('username')}", password=f"{form.cleaned_data.get('password1')}")
        if user is not None:
            return HttpResponseRedirect(f'/profile/{form.cleaned_data.get("username")}')
        return HttpResponseRedirect('login')
    return render(request, template, context)

def profile(request, username):
    profile = get_object_or_404(get_user_model().objects, username=username)
    posts = Post.objects.select_related('author').filter(
        author=profile).order_by('-pub_date')

    template = 'blog/profile.html'
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'profile': profile, 'page_obj': page_obj}
    return render(request, template, context)



# class ProfileView(DetailView):
#     model = get_user_model()
#     template_name = 'blog/profile.html'
#     slug_field = 'username'
#     slug_url_kwarg = 'username'
#     query_pk_and_slug = True
#     context_object_name = 'profile'



    def get_context_data(self, *args, **kwargs):
        # Get the existing context dictionary, then add
        # your custom object to it before returning it
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        context['object_list'] = Post.objects.select_related('author').filter(author__username=kwargs['object'].username).exclude(is_published=False, pub_date__gte=timezone.now(), category__is_published=False)
        context['is_paginated'] = True
        context['paginator'] = Paginator
        #context['page_obj'] = object_list
        context_update = {'paginator': django.core.paginator.Paginator, 'is_paginated': True}
        #context.update(context_update)
        #context['profile'] = get_object_or_404(get_user_model().objects, username=kwargs['object'].username)
        return context


    def __str__(self):
        return get_user_model().username


def edit_profile(request, pk=None):
    instance = get_object_or_404(get_user_model(), username=request.user)
    form = ProfileForm(request.POST or None, instance=instance)
    context = {'form': form}

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(f'profile/{request.user}')

    return render(request, 'blog/user.html', context)