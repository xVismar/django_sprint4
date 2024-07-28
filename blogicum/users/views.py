from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView


class UserRegistView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm




class ProfileView(DetailView):
    template_name = 'blog/profile.html'
    ordering = 'id'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.commentary.select_related('author')
        )
        return context

