from rest_framework import serializers

from django.contrib.auth.models import User
from polls.models import Question, Choice

class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.ReadOnlyField(source='question.creator.username')
    question = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='question-detail'
    )

    class Meta:
        model = Choice
        fields = ('url', 'id', 'choice_text', 'votes', 'creator', 'question')

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    choice_set = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='choice-detail',
        read_only=True)

    class Meta:
        model = Question
        fields = ('url', 'question_text', 'pub_date', 'was_published_recently', 'choice_set', 'creator')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # questions = QuestionSerializer(many=True, read_only=True)
    questions = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='question-detail',
        read_only=True)
        
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'questions')
