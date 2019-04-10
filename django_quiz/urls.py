"""django_quiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView
from django.views.static import serve
from django.views.decorators.csrf import csrf_exempt

from django_quiz import settings
from quiz_app import views as quiz_views
from spell_bee import views as sb_views
from rapid_fire import views as rf_views

urlpatterns = [
    url(r'^$', quiz_views.index, name='index'),

    # Team URLs
    url(r'^team/', quiz_views.team_intro, name='team_intro'),

    # Spell Bee URLs
    url(r'^quiz/spellbee/$', sb_views.sb_quiz_info, name='sb_quiz_info'),
    url(r'^quiz/spellbee/question', sb_views.sb_question, name='sb_question'),

    # Rapid Fire URLs
    url(r'^quiz/rapidfire/$', rf_views.rf_quiz_info, name='rf_quiz_info'),
    url(r'^quiz/rapidfire/question', rf_views.rf_question, name='rf_question'),

    # MCQ Quiz URLs
    url(r'^quiz/(.+)/question', quiz_views.question, name='question'),
    url(r'^quiz/(.+)$', quiz_views.quiz_info, name='rf_quiz_info'),
    url(r'^quiz/', quiz_views.spin_quiz, name='spin_quiz'),

    # Score URLs
    url(r'scoreboard/', quiz_views.score_board, name='score_board'),
    url(r'api/score/', csrf_exempt(quiz_views.ScoreAPI.as_view()), name='score_api'),
    url(r'resetscore', RedirectView.as_view(url='/api/score?reset=1',permanent=False)),

    # Outbox API
    url(r'api/outbox', quiz_views.OutBoxAPI.as_view(), name='outbox_api'),

    # Print Quiz Questions
    url(r'^print/(.+)$', quiz_views.print_quiz, name='print_quiz'),

    # Fillers page
    url(r'fillers/$', quiz_views.choose_filler, name='filler_page'),

    url(r'^admin/', admin.site.urls),
    url(r'navigation', quiz_views.navigation, name='navigation'),
]

urlpatterns.append(url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}))
