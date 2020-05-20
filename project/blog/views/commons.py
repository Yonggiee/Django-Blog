from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def add_login_context(context):
    context['login_form'] = AuthenticationForm()
    return context

def handle_login(request):
    username = request.POST['username']
    password = request.POST['password']
    new_user = authenticate(username=username, password=password)
    login(request, new_user)
