from django.shortcuts import render, redirect

from quiz_app.models import get_default_background, Team
from spell_bee.models import *

QUIZ = QuizInfo.objects.all()[0]
QUESTIONS = SpellBeeQuestion.objects.all()


def sb_quiz_info(request):
    print(QUIZ.get_background_image_url())
    context = {
        'quiz': QUIZ,
        'is_sb': True,
        'questions': QUESTIONS,
        'background_img': QUIZ.get_background_image_url()
    }
    return render(request, 'sb_info.html', context)


def sb_question(request):
    print("SEE MEE")
    questions = list(QUESTIONS)
    teams = Team.objects.all()
    background_image = QUIZ.get_background_image_url()
    media_asset = None

    try:
        get = request.GET
    except:
        pass

    try:
        q_number = get["qid"]
    except:
        if questions:
            q_number = questions[0].id
        else:
            q_number = None

    if q_number:
        try:
            question = QUESTIONS.get(question_number=q_number)
        except:
            return redirect("/quiz")
    else:
        question = "No questions"

    if not isinstance(question, str):
        # Select team
        number_of_teams = len(teams)
        q_num = question.question_number
        if q_num <= number_of_teams:
            team = teams[q_num - 1]
        else:
            team = teams[(q_num - 1) % number_of_teams]
    else:
        team = ""

    context = {
        'quiz': QUIZ,
        'question': question,
        'time': QUIZ.get_time(),
        'teams': ",".join([t.name for t in teams]),
        'team': team,
        'increment': QUIZ.get_increment(),
        'decrement': QUIZ.get_decrement(),
        'background_img': background_image
    }

    return render(request, 'sb_question.html', context)
