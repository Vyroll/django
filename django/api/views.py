from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework import permissions
from django.contrib.auth.models import User
from polls.models import Question, Choice
from .serializers import UserSerializer, QuestionSerializer, ChoiceSerializer
from .permissions import IsCreatorOrReadOnly

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsCreatorOrReadOnly,)


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def perform_create(self, serializer):
        serializer.save(question=self.request.question)