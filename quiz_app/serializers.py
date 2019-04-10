from rest_framework import serializers

from quiz_app.models import QuizScore, Question, Quiz
from rapid_fire.models import RapidFireScore
from spell_bee.models import QuizInfo, SpellBeeScore


class QuizScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizScore
        fields = '__all__'


class SpellBeeScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellBeeScore
        fields = '__all__'

class RapidFireScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = RapidFireScore
        fields = '__all__'


class OutBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
