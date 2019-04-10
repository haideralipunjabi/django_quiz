from django.contrib import admin

from spell_bee.models import *

class SpellBeeAdmin(admin.ModelAdmin):
    change_form_template = 'admin/quiz/change_form.html'
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['printURL'] = "/print/spellbee"
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

class SpellBeeQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'word', 'usage')
    ordering = ('question_number',)


class SpellBeeScoreAdmin(admin.ModelAdmin):
    list_display = ('team', 'score')
    ordering = ('team',)

admin.site.register(SpellBeeQuestion, SpellBeeQuestionAdmin)
admin.site.register(QuizInfo,SpellBeeAdmin)
admin.site.register(SpellBeeScore, SpellBeeScoreAdmin)
