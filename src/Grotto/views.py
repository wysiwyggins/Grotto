from urllib.parse import urlparse

from django import forms
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.mixins import LoginRequiredMixin as BaseLoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect, render, resolve_url
from django.views.generic import FormView, TemplateView


def index(request):
    return render(request, "static_pages/index.html")


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username",)
        field_classes = {"username": UsernameField}


class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = "/guild/"

    def form_valid(self, form):
        form.save()
        # log in the user here!
        user = authenticate(
            self.request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return super().form_valid(form)


class TermsAcceptForm(forms.Form):
    accept_terms = forms.BooleanField()


class TermsAcceptView(BaseLoginRequiredMixin, FormView):
    form_class = TermsAcceptForm
    success_url = "/guild/"
    template_name = "registration/accept_terms.html"

    def form_valid(self, form):
        print(form.cleaned_data)
        if form.cleaned_data["accept_terms"] is True:
            self.request.user.accepts_terms = True
            self.request.user.save()
        return super().form_valid(form)


class ActionMixin:
    """Puts action details on bottom of template"""

    actions = [
        {
            "url": "#",
            "text": "demo action 1",
        },
        {
            "url": "#",
            "text": "demo action 2",
        },
        {
            "url": "#",
            "text": "demo action 3",
        },
    ]

    def formatted_actions(self):
        """Hook for doing whatever mutation on actions that might be necessary"""
        return self.actions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"actions": self.formatted_actions()})
        return context


class UserAcceptsTermsMixin(UserPassesTestMixin):
    login_url = "/terms/"

    def test_func(self):
        return self.request.user.is_anonymous or self.request.user.accepts_terms

    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        # If the login url is the same scheme and net location then use the
        # path as the "next" url.
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
            not login_netloc or login_netloc == current_netloc
        ):
            path = self.request.get_full_path()
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )


class LoginRequiredMixin(BaseLoginRequiredMixin, UserAcceptsTermsMixin):
    pass
