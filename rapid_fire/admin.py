from django.contrib import admin

from rapid_fire.models import RapidFireQuestion, RapidFireScore
from rapid_fire.models import RapidFireQuiz


class RapidFireAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'questions_per_team')
    change_form_template = 'admin/quiz/change_form.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['printURL'] = "/print/rapidfire"
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

class RapidFireQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'content')
    list_display_links = ('content',)
    ordering = ('question_number',)


class RapidFireScoreAdmin(admin.ModelAdmin):
    list_display = ('team', 'score')
    ordering = ('team',)


admin.site.register(RapidFireQuiz, RapidFireAdmin)
admin.site.register(RapidFireQuestion, RapidFireQuestionAdmin)
admin.site.register(RapidFireScore, RapidFireScoreAdmin)