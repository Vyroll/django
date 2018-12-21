from rest_framework import serializers

from django.contrib.auth.models import User
from polls.models import Question, Choice
from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='snippet-detail',
        read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    choice_set = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='choice-detail',
        read_only=True)

    class Meta:
        model = Question
        fields = ('question_text', 'pub_date', 'was_published_recently', 'choice_set')

class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    question = serializers.ReadOnlyField(source='question.question_text')

    class Meta:
        model = Choice
        fields = ('url', 'id', 'choice_text', 'question', 'votes')