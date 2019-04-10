from django.contrib import admin
from .models import *


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2


class OptionInline(admin.StackedInline):
    model = Option
    extra = 2


class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'max_questions', 'enabled')
    search_fields = ('question', 'quiz',)
    inlines = [QuestionInline]
    change_form_template = 'admin/quiz/change_form.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        quiz = Quiz.objects.get(id=object_id)
        extra_context['printURL'] = "/print/"+quiz.title
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'content', 'quiz')
    list_display_links = ('content',)
    ordering = ('quiz', 'question_number')
    inlines = [OptionInline]


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('team', 'score')
    ordering = ('team',)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo_preview')
    list_display_links = ('name',)
    ordering = ('name',)


class FillerAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
admin.site.register(Filler, FillerAdmin)
admin.site.register(LayoutAssets)
admin.site.register(Team, TeamAdmin)
admin.site.register(QuizScore, ScoreAdmin)
