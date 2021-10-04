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
            "url": "/guild/crypt/",
        }
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user, dead=False)
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
            "text": "Go to Guild Hall",
            "url": "/guild/",
        },
        {
            "text": "Enter the Grotto",
            "url": "/game/become/{character_pk}/",
            "become": True,
        },
        {
            "text": "Roll New Character",
            "url": "/guild/test/",
        },
    ]

    def formatted_actions(self):
        _formatted = []
        for action in self.actions:
            if action.get("become", False) and not self.is_players_character:
                # Don't put a link to enter the grotto unless this is your character
                continue
            _formatted.append({
                "text": action["text"],
                "url": action["url"].format(character_pk=self.character_pk),
            })
        return _formatted

    def get(self, request, *args, **kwargs):
        self.character_pk = kwargs["pk"]
        self.is_players_character = Character.objects.filter(user=request.user, id=kwargs["pk"]).exists()
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
    alt_actions = [{"text": "View Character", "url": "/guild/new-character/"}]

    def get_context_data(self, satisfied=False, another=False, **kwargs):
        asked = []
        _asked = self.request.session.get("questions_asked")
        if _asked:
            asked = [int(q) for q in _asked.split(",")]
        pks = CharacterTest.objects.exclude(id__in=asked).values_list("id", flat=True).order_by("id")
        ctx = {}
        if not pks or satisfied:
            self.actions = self.alt_actions
            self.request.session["questions_asked"] = None
        else:
            random_pk = choice(pks)
            character_test = CharacterTest.objects.get(id=random_pk)
            ctx.update(
                {
                    "question": character_test.question,
                    "answer_choices": character_test.choices.all(),
                    "another": another,
                }
            )
            asked.append(random_pk)
            self.request.session["questions_asked"] = ",".join([str(q) for q in asked])

        context = super().get_context_data(**kwargs)
        context.update(ctx)
        return context

    def post(self, request, *args, **kwargs):
        # possibly validate that form a little bit
        # roll a D20
        roll = randint(1, 20)
        if roll > 12:
            # enough questions answered
            context = self.get_context_data(satisfied=True)
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


class CryptView(LoginRequiredMixin, ActionMixin, ListView):
    template_name = "crypt.html"
    model = Character
    actions = [{
            "url": "/guild/",
            "text": "Return to guild hall",
        }]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(dead=True)
        return queryset


