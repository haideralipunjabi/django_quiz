from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import PROTECT
from django.db.models.signals import m2m_changed
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils.safestring import mark_safe

from utils.utils import validate_only_one_instance, get_default_background


# Layout models

class LayoutAssets(models.Model):
    intro_background_image = models.ImageField(blank=True, null=True)
    team_intro_background = models.ImageField(blank=True, null=True)

    def get_homepage_url(self):
        # return self.homepage_background_image.url
        return self.homepage_intro_video.url

    def get_intro_url(self):
        return self.intro_background_image.url

    def get_quiz_chooser_background(self):
        return self.quiz_chooser_background.url

    def get_score_board_background(self):
        return self.score_board_background.url if self.score_board_background else get_default_background()

    def get_team_intro_background(self):
        return self.team_intro_background.url if self.team_intro_background else get_default_background()

    def clean(self):
        validate_only_one_instance(self)


# Team

class Team(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(
        max_length=70,
        help_text="Team name")
    description = models.TextField(
        max_length=700,
        help_text="Team description")
    photo = models.ImageField(help_text="Intro image for the team.")

    score_record = models.CharField(
        blank=True,
        null=True,
        max_length=1000,
        help_text="A score record of the team progress. DO NOT MESS WITH THIS!")

    def photo_preview(self):
        return mark_safe('<img src="%s" alt="Image" width="100px" height="100px" />' % self.get_image_url())

    def get_image_url(self):
        return self.photo.url

    def get_name(self):
        return self.name

    def get_description(self):
        print(type(self.description))
        return self.description

    def get_team_background(self):
        return settings.STATIC_URL + "team_intro_background.jpg"


class Filler(models.Model):
    name = models.CharField(
        max_length=50,
        help_text="Title of the video")
    video = models.FileField(help_text="The filler video")

    def get_video(self):
        return self.video.url


# Quiz models

class Quiz(models.Model):
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

    random_order = models.BooleanField(
        default=True,
        help_text="Display the questions in a randomized order instead of following the sequence as is.")

    max_questions = models.IntegerField(
        default=15,
        help_text="Maximum number of questions to be displayed in a single quiz sitting")

    increment_per_question = models.IntegerField(
        default=5,
        help_text="The increment to be made in the score per right answer.")

    negative_score = models.IntegerField(
        default=-1,
        help_text="The decrement to be made in the score per wrong answer (Include the minus '-' sign)."
    )

    timer = models.IntegerField(
        default=0,
        help_text="Time limit per question. Set 0 to disable timer.")

    success_message = models.CharField(
        max_length=70,
        default="Well done!",
        help_text="A success message to be displayed when the right answer is selected.")

    fail_message = models.CharField(
        max_length=70,
        default="Uh-Oh!",
        help_text="The message to be displayed if the user fails to answer correctly.")

    enabled = models.BooleanField(
        default=True,
        help_text="Whether or not the quiz should be accessible.")

    # scores = GenericRelation(Score, related_query_name='scores_q')

    def get_questions(self):
        return self.question_set.all()

    def get_max_score(self):
        pass

    def get_increment(self):
        return self.increment_per_question

    def get_decrement(self):
        return self.negative_score

    def get_time(self):
        return self.timer

    def get_background_image_url(self):
        return self.background_image.url

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")


'''class QuizObject(models.Model):
    CHOICES = (
        (ContentType.objects.get_for_model(Quiz), "Quiz"),
        (ContentType.objects.get_for_model(QuizInfo), "Spell Bee Quiz")
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.pythCASCADE, choices=CHOICES)
    object_id = models.PositiveIntegerField(help_text="ID of the quiz this score is associated with.")
    content_object = GenericForeignKey('content_type', 'object_id')


class Score(models.Model):
    team = models.ForeignKey(Team)
    score = models.IntegerField(default=0)
    quiz = GenericRelation(QuizObject)'''


class QuizScore(models.Model):
    team = models.ForeignKey(Team, on_delete=PROTECT)
    score = models.IntegerField(default=0)
    quiz = models.ForeignKey(Quiz, on_delete=PROTECT)


class Question(models.Model):
    def __str__(self):
        return "[" + self.quiz.title + "] " "Q." + str(self.question_number) + " " + self.content

    quiz = models.ForeignKey(
        Quiz,
        help_text="The quiz this question belongs to.", on_delete=PROTECT)

    question_number = models.IntegerField(help_text="Question number (relative to current quiz).")

    content = models.CharField(
        max_length=500,
        help_text="The question.",
        unique=True)

    explanation = models.CharField(
        max_length=500,
        help_text="An explanation to display after showing the correct answer to the question.",
        blank=True,
        null=True)

    image_asset = models.ImageField(
        help_text="An image asset related to the question",
        blank=True,
        null=True)

    audio_asset = models.FileField(
        help_text="Audio asset for the given question.",
        blank=True,
        null=True, )

    video_asset = models.FileField(
        help_text="Video asset for this question",
        blank=True,
        null=True, )

    '''
    def clean(self, options=()):
        if not options:
            options = self.options.all()
        print(options)
        answer = self.answer
        if answer not in options:
            raise ValidationError("The answer must be one of the options of the question.")
    '''

    def clean(self):
        quiz = self.quiz
        questions = quiz.question_set.all()
        # Check for question number
        for question in questions:
            if question.question_number == self.question_number and self != question:
                raise ValidationError("Question number must be unique.")
        # Check for multiple media assets
        medias = []
        try:
            if self.image_asset:
                medias.append(self.image_asset)
        except:
            pass

        try:
            if self.audio_asset:
                medias.append(self.audio_asset)
        except:
            pass

        try:
            if self.video_asset:
                medias.append(self.video_asset)
        except:
            pass

        if len(medias) > 1:
            raise ValidationError("Each question should have only one media asset.")

    def get_media_asset(self):
        media = None
        try:
            media = self.image_asset.url
        except:
            pass
        try:
            media = self.video_asset.url
        except:
            pass
        try:
            media = self.audio_asset.url
        except:
            pass
        return media

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")


class Option(models.Model):
    def __str__(self):
        return self.content

    question = models.ForeignKey(Question, help_text="The question this option belongs to.",on_delete=PROTECT)
    is_correct = models.BooleanField(default=False, help_text="Is this the right option?")
    content = models.CharField(
        max_length=70,
        help_text="The option.")

    class Meta:
        verbose_name = _("option")
        verbose_name_plural = _("options")


'''
def validate_question(sender, instance, **kwargs):
    # Check if there is at least one correct option
    has_correct = False
    options = instance.option_set.all()
    for option in options:
        print(option, option.is_correct)
        if option.is_correct:
            has_correct = True
    if not has_correct:
        raise ValidationError("Question must have at least one valid answer")

models.signals.pre_save.connect(validate_question, sender=Question)
'''
