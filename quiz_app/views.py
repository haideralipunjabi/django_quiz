import json
import random

import simplejson as simplejson
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from quiz_app.serializers import QuizScoreSerializer, OutBoxSerializer, SpellBeeScoreSerializer, \
    RapidFireScoreSerializer
from rapid_fire.models import RapidFireQuiz, RapidFireScore, RapidFireQuestion
from spell_bee.models import QuizInfo, SpellBeeScore, SpellBeeQuestion
from .models import *

LAYOUT_ASSET = LayoutAssets.objects.all()[0]
outbox = {}
used_questions = []


def get_quiz_questions(quiz):
    """ Fetches <= quiz.max_questions number of questions from the given quiz """
    max_questions = quiz.max_questions
    questions = quiz.question_set.all().order_by('question_number')
    if len(questions) > max_questions:
        outbox[quiz.title] = questions[max_questions:len(questions)]
        questions = questions[0:max_questions]
    else:
        outbox[quiz.title] = []
    return questions


def get_outbox_question(quiz_title):
    """ Returns a question from the outbox of the given quiz """
    quiz_outbox = outbox[quiz_title]
    if len(quiz_outbox):
        question = random.choice(outbox[quiz_title])
        quiz_outbox.remove(question)
    else:
        question = None
    if question:
        used_questions.append(question)
    # print("USED QUESTIONS", used_questions)
    return question


def update_out_box():
    """ Updates the outbox """
    for quiz in Quiz.objects.all():
        get_quiz_questions(quiz)
        print("Generated outbox for", quiz, "| Questions: ", len(outbox[quiz.title]))
    for quiz in outbox:
        new_copy = outbox[quiz].copy()
        for question in outbox[quiz]:
            # Debugging
            # if quiz == "Chemistry":
            # print("OUTBOX:", outbox[quiz])
            # print("IN CHEMISTRY")
            # print("IN UPDATE", question)
            # print("IN UPDATE:USED QUESTIONS", used_questions)
            # print("IN UPDATE", question.content in [q.content for q in used_questions])
            if question in used_questions:
                print("REMOVED", question)
                new_copy.remove(question)
        outbox[quiz] = new_copy


update_out_box()


def index(request):
    intro_image_source = LAYOUT_ASSET.get_intro_url()
    context = {
        "show": "intro",
        "intro_img_src": intro_image_source
    }
    return render(request, 'index.html', context)


def team_intro(request):
    try:
        get = request.GET
    except:
        team = ""
        current = ""

    try:
        team = get['team']
    except:
        team = ""

    try:
        current = get['current']
    except:
        current = ""

    teams = list(Team.objects.all())
    default_team = Team.objects.all()[0]

    if not team:
        team = default_team.name

    try:
        team_object = Team.objects.get(name=team)
    except:
        team_object = default_team

    last_team = False
    print(team)
    if team == "next":
        teamobj = Team.objects.get(name=current)
        new_in = teams.index(teamobj) + 1
        print(new_in)
        if new_in == len(teams) - 1:
            last_team = True
        print("YES")
        team_object = teams[new_in]

    background_image = LAYOUT_ASSET.get_team_intro_background()
    team_object.description = team_object.description.split("\n")
    context = {
        "team": team_object,
        "last_team": last_team,
        "background_img": background_image
    }

    return render(request, 'team.html', context)


def choose_filler(request):
    fillers = Filler.objects.all()
    context = {
        "fillers": fillers
    }
    return render(request, 'fillers.html', context)


def choose_quiz(request):
    quizzes = Quiz.objects.filter(enabled=True)
    first_half = quizzes[0:int((len(quizzes) + 1) / 2)]
    second_half = quizzes[len(first_half):len(quizzes)]
    background_img = LAYOUT_ASSET.get_quiz_chooser_background()
    context = {
        'quizzes': quizzes,
        'first_half': first_half,
        'second_half': second_half,
        'background_img': background_img,
    }
    return render(request, 'quizzes.html', context)


def spin_quiz(request):
    quizzes = Quiz.objects.filter(enabled=True)
    context = {
        'quizzes': quizzes,
    }
    return render(request, 'spinner.html', context)


def print_quiz(request, quiz_name):
    is_sb = quiz_name.lower() == "spellbee"
    is_rf = quiz_name.lower() == "rapidfire"
    quiz = None
    quiz_outbox = None

    if quiz_name.lower() not in ["spellbee", "rapidfire"]:
        quiz = Quiz.objects.get(title=quiz_name)
    else:
        if is_sb:
            questions = SpellBeeQuestion.objects.all()
        elif is_rf:
            questions = RapidFireQuestion.objects.all()

    if quiz:
        quiz_outbox = outbox[quiz.title]
        questions = list(set(quiz.question_set.all()) - set(quiz_outbox))

    context = {
        'quiz': quiz_name,
        'questions': questions,
        'outbox': quiz_outbox,
        'is_sb': is_sb,
        'is_rf': is_rf
    }

    return render(request, 'print_quiz.html', context)


def quiz_info(request, quiz_name):
    quiz = Quiz.objects.filter(title=quiz_name)[0]
    max_questions = quiz.max_questions
    questions = get_quiz_questions(quiz)
    if len(questions) > max_questions:
        outbox[quiz.title] = questions[max_questions:len(questions) - 1]
        questions = questions[0:max_questions]
    print(outbox)
    background_image = quiz.get_background_image_url()
    context = {
        'quiz': quiz,
        'questions': questions,
        'background_img': background_image
    }
    return render(request, 'quiz_info.html', context)


def question(request, quiz_name):
    quiz = Quiz.objects.filter(title=quiz_name)[0]
    questions = list(get_quiz_questions(quiz))
    teams = Team.objects.all()
    background_image = quiz.get_background_image_url()
    media_asset = None
    timer = quiz.get_time()

    try:
        get = request.GET
    except:
        pass

    try:
        q_number = get["qid"]
    except:
        if questions:
            q_number = questions[0].question_number
        else:
            q_number = None

    if q_number:
        try:
            for q in questions:
                if int(q.question_number) == int(q_number):
                    question = q
                    print(question)
            if not question:
                redirect("/quiz")
        except:
            return redirect("/quiz")
    else:
        question = "No questions"

    if not isinstance(question, str):
        explanation = question.explanation
        options = question.option_set.all()
        first_half = options[0:int((len(options) + 1) / 2)]
        second_half = options[len(first_half):len(options)]
        media_asset = question.get_media_asset()
        # Select team
        number_of_teams = len(teams)
        q_num = question.question_number
        if q_num <= number_of_teams:
            team = teams[q_num - 1]
        else:
            team = teams[(q_num - 1) % number_of_teams]
            explanation = ""
    else:
        question = "No question"
        first_half = ""
        second_half = ""
        team = ""
        explanation = ""

    context = {
        'quiz': quiz,
        'question': question,
        'explanation': explanation,
        'teams': ",".join([t.name for t in teams]),
        'team': team,
        'time': timer,
        'first_half': first_half,
        'second_half': second_half,
        'increment': quiz.get_increment(),
        'decrement': quiz.get_decrement(),
        'media_asset': media_asset,
        'background_img': background_image
    }

    return render(request, 'question.html', context)


def score_board(request):
    quiz_score_objects = QuizScore.objects.all()
    sb_score_objects = SpellBeeScore.objects.all()
    rf_score_objects = RapidFireScore.objects.all()
    team_score_dict = {}
    team_id_dict = {}
    teams = []

    for score_obj in quiz_score_objects:
        if score_obj.team.name in team_score_dict:
            team_score_dict[score_obj.team.name] += score_obj.score
        else:
            team_score_dict[score_obj.team.name] = score_obj.score

        teams.append(score_obj.team)

    for sb_score_obj in sb_score_objects:
        if sb_score_obj.team.name in team_score_dict:
            team_score_dict[sb_score_obj.team.name] += sb_score_obj.score
        else:
            team_score_dict[sb_score_obj.team.name] = sb_score_obj.score

    for rf_score_obj in rf_score_objects:
        if rf_score_obj.team.name in team_score_dict:
            team_score_dict[rf_score_obj.team.name] += rf_score_obj.score
        else:
            team_score_dict[rf_score_obj.team.name] = rf_score_obj.score

        if not sb_score_obj.team in teams:
            teams.append(sb_score_obj.team)

    # Sort the teams according to their IDs in the database
    for team in teams:
        team_id_dict[team.id] = team.name

    sorted_score_dict = {}

    for key in sorted(team_id_dict):
        sorted_score_dict[team_id_dict[key]] = team_score_dict[team_id_dict[key]]

    # print(sorted_score_dict, team_id_dict)

    context = {
        'team_score_dict': sorted_score_dict,
    }
    return render(request, 'score_board.html', context)


def navigation(request):
    return render(request, 'navigation.html', context=None)


class ScoreAPI(APIView):
    def get(self, request):
        try:
            reset = int(request.GET['reset'])
        except:
            reset = False

        print(reset)
        # Delete score records
        if reset:
            print(reset, "RESETTING SCORES")
            QuizScore.objects.all().delete()
            SpellBeeScore.objects.all().delete()
            RapidFireScore.objects.all().delete()
            for team in Team.objects.all():
                team.score_record = None
                team.save()

        returnData = []
        data = {}
        per_quiz_data = {}
        sb_quiz = QuizInfo.objects.all()[0]
        rf_quiz = RapidFireQuiz.objects.all()[0]

        team_quiz_data = {}

        # Ensure score objects exist
        for quiz in Quiz.objects.all():
            for team in Team.objects.all():
                QuizScore.objects.get_or_create(team=team, quiz=quiz)

        for team in Team.objects.all():
            quiz_score_data = {}
            sb_scores, dummy = SpellBeeScore.objects.get_or_create(team=team, quiz=sb_quiz)
            rf_scores, dummy = RapidFireScore.objects.get_or_create(team=team)
            team_scores = QuizScore.objects.filter(team=team)
            for score in team_scores:
                quiz_score_data[score.quiz.title] = score.score
            quiz_score_data[sb_quiz.title] = sb_scores.score
            quiz_score_data[rf_quiz.title] = rf_scores.score
            team_quiz_data[team.name] = quiz_score_data

        sb_quiz_data = {}
        rf_quiz_data = {}

        for team in Team.objects.all():
            score_obj, dummy = SpellBeeScore.objects.get_or_create(team=team, quiz=sb_quiz)
            sb_quiz_data[team.name] = score_obj.score

        for team in Team.objects.all():
            score_obj, dummy = RapidFireScore.objects.get_or_create(team=team)
            rf_quiz_data[team.name] = score_obj.score

        per_quiz_data[sb_quiz.title] = sb_quiz_data
        per_quiz_data[rf_quiz.title] = rf_quiz_data

        data['scores'] = team_quiz_data

        team_score_change = {}
        for team in Team.objects.all():
            team_score_change[team.name] = team.score_record
        data['team_score_change'] = team_score_change
        returnData.append(data)
        response = Response(data)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
        return response

    def post(self, request):
        data = dict(request.POST)
        print(data)
        change = data['score'][0]
        print(data)
        team = Team.objects.get(name=data['team'][0])
        data['team'] = team.id
        is_sb = False  # Quiz is spellbee?
        is_rf = False  # Quiz is rapid fire?
        if data['quiz'][0] == QuizInfo.objects.all()[0].title:
            quiz = QuizInfo.objects.all()[0]
            is_sb = True
        elif data['quiz'][0] == RapidFireQuiz.objects.all()[0].title:
            quiz = RapidFireQuiz.objects.all()[0]
            is_rf = True
        else:
            quiz = Quiz.objects.get(title=data['quiz'][0])

        if not is_rf:
            data['quiz'] = quiz.id
        else:
            data.pop('quiz')

        if is_sb:
            score_obj, dummy = SpellBeeScore.objects.get_or_create(
                team=team,
                quiz=quiz)
        elif is_rf:
            score_obj, dummy = RapidFireScore.objects.get_or_create(team=team)
        else:
            score_obj, dummy = QuizScore.objects.get_or_create(
                team=team,
                quiz=quiz)
        print(score_obj.score)
        data['score'] = score_obj.score + int(change)
        data['id'] = score_obj.id
        # Update score records
        if not team.score_record:
            team.score_record = '0,' + str(change)
        else:

            team.score_record += ", " + str(change)
        team.save()

        # print("SEE ME", change, team.score_record)
        if is_sb:
            serializer = SpellBeeScoreSerializer(score_obj, data=data, partial=True)
        elif is_rf:
            serializer = RapidFireScoreSerializer(score_obj, data=data, partial=True)
        else:
            serializer = QuizScoreSerializer(score_obj, data=data, partial=True)
        print(serializer.is_valid())
        print(data)
        if serializer.is_valid():
            print("IS VALID")
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "GET, OPTIONS, POST"
            response["Access-Control-Max-Age"] = "1000"
            response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
            return response

        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS, POST"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
        return response


class OutBoxAPI(APIView):
    def get(self, request):
        try:
            data = request.GET
        except:
            data = {'quiz_name': None}
        update_out_box()
        quiz_title = data['quiz_name']
        question = get_outbox_question(quiz_title)
        options = question.option_set.all()
        for opt in options:
            if opt.is_correct:
                correct_option = opt.content
        return_json = {
            "content": question.content,
            "question_number": question.question_number,
            "quiz": question.quiz.title,
            "explanation": question.explanation,
            "media_asset": question.get_media_asset(),
            "options": [opt.content for opt in options],
            "correct": correct_option,
        }
        response = Response(return_json, status=status.HTTP_201_CREATED)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS, POST"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
        update_out_box()
        return response
