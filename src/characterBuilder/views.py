from random import choice, randint

from django import forms
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import FormView, RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from Grotto.views import ActionMixin, LoginRequiredMixin

from .character_generator import Character as CharacterGenerator
from .models import Character, CharacterTest, CharacterTestChoice

# Create your views here.


class Index(LoginRequiredMixin, ActionMixin, ListView):
    template_name = "guild.html"
    model = Character
    paginate_by = 25
    actions = [
        {
            "text": "Speak to Crone (Create Character)",
            "url": "/guild/test/",
        },

        {
            "text": "Visit the Crypt",
            "url": "/crypt/",
        }
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class CharacterDetailView(LoginRequiredMixin, ActionMixin, DetailView):
    model = Character
    template_name = "character.html"
    query_pk_and_slug = True
    actions = [
        {
            "text": "Enter the Grotto",
            "url": "/game/enter/",
        },
        {
            "text": "Reroll Character",
            "url": "/guild/test/",
        },
    ]

    def get(self, request, *args, **kwargs):
        request.session["character_pk"] = kwargs["pk"]
        return super().get(request, *args, **kwargs)


class CharacterTestView(LoginRequiredMixin, ActionMixin, TemplateView):
    template_name = "character_test.html"
    actions = [
        {
            "url": "/guild/test/",
            "text": "Take a different test",
        },
        {
            "url": "/guild/write-test/",
            "text": "Create a test",
        },
    ]

    def get_context_data(self, empty=False, another=False, **kwargs):
        context = super().get_context_data(**kwargs)
        if not empty:
            pks = CharacterTest.objects.values_list("id", flat=True).order_by("id")
            random_pk = choice(pks)
            character_test = CharacterTest.objects.get(id=random_pk)
            context.update(
                {
                    "question": character_test.question,
                    "answer_choices": character_test.choices.all(),
                    "another": another,
                }
            )
        return context

    def post(self, request, *args, **kwargs):
        # possibly validate that form a little bit
        # roll a D20
        roll = randint(1, 20)
        if roll > 12:
            # enough questions answered
            self.actions = [{"text": "View Character", "url": "/guild/new-character/"}]
            context = self.get_context_data(empty=True)
            return self.render_to_response(context)
        # otherwise ask another question
        context = self.get_context_data(another=True)
        return self.render_to_response(context)


class NewCharacterView(LoginRequiredMixin, RedirectView):
    pattern_name = "characterBuilder:character"

    def get(self, request, *args, **kwargs):
        # actually create the character and associate to user
        character = CharacterGenerator().generateCharacter(user=request.user)
        kwargs.update({"pk": character.pk})
        return super().get(request, *args, **kwargs)


class CharacterTestCreateView(LoginRequiredMixin, ActionMixin, TemplateView):
    template_name = "character_test_create.html"

    def post(self, request, *args, **kwargs):
        errors = []
        context = self.get_context_data()
        question = request.POST.get("question", "").strip()
        if not question:
            errors.append("you must ask a question")
        answers = [a for a in request.POST.getlist("answer") if a.strip()]
        if len(answers) < 2:
            errors.append("you must provide at least two answers")
        if errors:
            context.update({"errors": errors})
            return self.render_to_response(context)
        # create the model instances
        test = CharacterTest.objects.create(question=question)
        for answer in answers:
            CharacterTestChoice.objects.create(character_test=test, choice=answer)
        return redirect("/guild/test/")
