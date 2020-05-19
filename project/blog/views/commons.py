from django.contrib.auth.forms import AuthenticationForm

def add_login_context(context):
    context['login_form'] = AuthenticationForm()
    return context