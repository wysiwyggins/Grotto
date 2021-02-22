from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'static_pages/index.html')

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username",)
        field_classes = {'username': UsernameField}


class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = "/guild/"

    def form_valid(self, form):
        form.save()
        # log in the user here!
        user = authenticate(self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(self.request, user)
        return super().form_valid(form)


class ActionMixin():
    """Puts action details on bottom of template"""
    actions = [{
        "url": "#",
        "text": "demo action 1",
    }, {
        "url": "#",
        "text": "demo action 2",
    }, {
        "url": "#",
        "text": "demo action 3",
    }]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"actions": self.actions})
        return context
