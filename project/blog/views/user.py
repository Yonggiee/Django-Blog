from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.views.generic.edit import CreateView

from user.forms import SignUpForm
from .commons import add_login_context

class UserCreateView(CreateView):
    form_class = SignUpForm
    template_name = 'user_new.html'

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        valid = super(UserCreateView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid

class UserLoginView(LoginView):
    template_name = 'user_login.html'

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data(**kwargs)
        context = add_login_context(context)
        return context

    def get_success_url(self):
        if 'next' in self.request.POST:
            return self.request.POST.get('next')
        else:
            return reverse('home')
    