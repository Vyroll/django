from django.conf.urls import url, include
from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter

from rest_framework.urlpatterns import format_suffix_patterns

# app_name = 'api' # can use because of DRF reverse implementation

router = DefaultRouter()
router.register('snippets', views.SnippetViewSet)
router.register('users', views.UserViewSet)
router.register('Question', views.QuestionViewSet)
router.register('Choice', views.ChoiceViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
