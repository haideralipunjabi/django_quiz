from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import PROTECT
from django.utils.translation import ugettext_lazy as _

from quiz_app.models import Team
from utils.utils import validate_only_one_instance


class QuizInfo(models.Model):
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

    timer = models.IntegerField(
        default=0,
        help_text="Time limit per question. Set 0 to disable timer.")

    background_image = models.ImageField(help_text="Background image for the quiz.", blank=True)

    increment_per_question = models.IntegerField(
        default=4,
        help_text="The increment to be made in the score per right answer.")

    negative_score = models.IntegerField(
        default=-1,
        help_text="The decrement to be made in the score per wrong answer (Include the minus '-' sign).")

    def get_background_image_url(self):
        return self.background_image.url

    def get_increment(self):
        return self.increment_per_question

    def get_decrement(self):
        return self.negative_score

    def get_time(self):
        return self.timer

    def clean(self):
        validate_only_one_instance(self)

    class Meta:
        verbose_name = _("Spell Bee Quiz Info")
        verbose_name_plural = _("Spell Bee Quiz Info")


class SpellBeeQuestion(models.Model):
    def __str__(self):
        return "Q" + str(self.question_number) + ". " + self.word

    question_number = models.IntegerField(
        unique=True,
        help_text="Question number")
    word_type = models.CharField(
        max_length=50,
        help_text="verb, noun, adjective etc.")
    word = models.CharField(
        unique=True,
        max_length=20,
        help_text="The word.")
    meaning = models.TextField(
        max_length=500,
        help_text="Meaning of the word.")
    usage = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        help_text="A sentence using the given word.")
    origin = models.CharField(
        max_length=70,
        default="",
        blank=True,
        null=True,
        help_text="Origin of word. latin etc.")
    audio = models.FileField(
        help_text="Audio pronunciation for the word.",
        blank=True,
        null=True)

    # scores = GenericRelation(Score, related_query_name='scores_sb')

    def get_audio_url(self):
        return self.audio.url if self.audio else None

    class Meta:
        verbose_name = _("Spell Bee Question")
        verbose_name_plural = _("spell Bee Questions")


class SpellBeeScore(models.Model):
    team = models.ForeignKey(Team,on_delete=PROTECT)
    score = models.IntegerField(default=0)
    quiz = models.ForeignKey(QuizInfo,on_delete=PROTECT)

    class Meta:
        verbose_name = _("Spell Bee Score")
        verbose_name_plural = _("spell Bee Scores")
