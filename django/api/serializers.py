from rest_framework import serializers

from django.contrib.auth.models import User
from polls.models import Question, Choice

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username')

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    choice_set = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='choice-detail',
        read_only=True)

    class Meta:
        model = Question
        fields = ('question_text', 'pub_date', 'was_published_recently', 'choice_set')

class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    # question_name = serializers.ReadOnlyField(source='question.question_text')
    question = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='question-detail'
    )

    class Meta:
        model = Choice
        fields = ('url', 'id', 'choice_text', 'votes', 
        # 'question_name', 
        'question',)