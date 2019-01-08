from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from polls.models import Question, Choice
from .serializers import UserSerializer, QuestionSerializer, ChoiceSerializer
from .permissions import IsCreatorOrReadOnly
from rest_condition import Or
from rest_framework_simplejwt.authentication import JWTAuthentication

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # permission_classes = (IsCreatorOrReadOnly,)
    # permission_classes = (Or(permissions.IsAuthenticated, TokenAuthentication),)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def perform_create(self, serializer):
        serializer.save(question=self.request.question)