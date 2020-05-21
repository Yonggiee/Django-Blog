from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def add_login_context(context):
    context['login_form'] = AuthenticationForm()
    return context

def handle_login(request):
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        login(request, form.get_user())
