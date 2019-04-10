from django.db import models
from django.db.models import SET_NULL, PROTECT
from django.utils.translation import ugettext_lazy as _

from quiz_app.models import Team
from utils.utils import validate_only_one_instance, get_default_background


class RapidFireQuiz(models.Model):
    def __str__(self):
        return self.title

    title = models.CharField(
        max_length=50,
        help_text="Quiz title e.g Math Storm!, Let's go Quantum!, The Hardest Quiz Ever!!!! etc.")

    description = models.CharField(
        max_length=200,
        help_text="Quiz description e.g 'A math quiz based on elementary school mathematics.'",
        null=True,
        blank=True)

    background_image = models.ImageField(help_text="Background image for the quiz.", blank=True)

    questions_per_team = models.IntegerField(
        default=15,
        help_text="Number of questions to be displayed per team")

    increment_per_question = models.IntegerField(
        default=4,
        help_text="The increment to be made in the score per right answer.")

    negative_score = models.IntegerField(
        default=-1,
        help_text="The decrement to be made in the score per wrong answer (Include the minus '-' sign)."
    )

    timer = models.IntegerField(
        default=0,
        help_text="Time limit per rapid fire round.")

    def get_background_image(self):
        return self.background_image.url if self.background_image else get_default_background()

    def get_increment(self):
        return self.increment_per_question

    def get_decrement(self):
        return self.negative_score

    def get_timer(self):
        return self.timer

    def clean(self):
        validate_only_one_instance(self)

    class Meta:
        verbose_name = _("Rapid Fire Quiz")
        verbose_name_plural = _("Rapid Fire Quiz")


class RapidFireQuestion(models.Model):
    def __str__(self):
        return "Q." + str(self.question_number) + " " + self.content

    question_number = models.IntegerField(help_text="Question number (relative to current quiz).", unique=True)
    content = models.CharField(
        max_length=500,
        help_text="The question.",
        unique=True)
    answer = models.CharField(
        max_length=100,
        help_text="Correct answer to the question",
    )

    class Meta:
        verbose_name = _("Rapid Fire Question")
        verbose_name_plural = _("Rapid Fire Questions")


class RapidFireScore(models.Model):
    team = models.ForeignKey(Team,on_delete=PROTECT)
    score = models.IntegerField(default=0)

    class Meta:
        verbose_name = _("Rapid Fire Score")
        verbose_name_plural = _("Rapid Fire Scores")
