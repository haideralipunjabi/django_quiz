import math
from django.shortcuts import render

from quiz_app.models import Team
from rapid_fire.models import RapidFireQuestion, RapidFireQuiz

QUIZ = RapidFireQuiz.objects.all()[0]
QUESTIONS_PER_TEAM = QUIZ.questions_per_team
QUESTIONS = [q.content for q in RapidFireQuestion.objects.all()]
number_of_teams = len(Team.objects.all())
max_questions = math.floor(len(QUESTIONS) / number_of_teams)
max_questions = max_questions if QUESTIONS_PER_TEAM > max_questions else QUESTIONS_PER_TEAM
quiz = RapidFireQuiz.objects.all()[0]
used_questions = []

print("[RF] MAX QUESTIONS", max_questions)


def get_questions():
    questions = None
    print(len(QUESTIONS), max_questions)
    if len(QUESTIONS) >= max_questions:
        questions = QUESTIONS[0:max_questions]
        for q in questions:
            QUESTIONS.remove(q)

    print(questions)
    print("MAX QUESTIONS", max_questions)
    return questions


def rf_question(request):
    context = {

    }
    context = {
        'quiz': QUIZ,
        'questions': get_questions(),
        'background_img': quiz.get_background_image(),
        'increment': QUIZ.get_increment(),
        'decrement': QUIZ.get_decrement(),
        'timer': QUIZ.get_timer()
    }
    return render(request, 'rf_question.html', context)


def rf_quiz_info(request):
    teams = Team.objects.all()
    background_img = quiz.get_background_image()
    context = {
        "teams": teams,
        "quiz": quiz,
        "background_img": background_img
    }
    return render(request, 'rf_info.html', context)
