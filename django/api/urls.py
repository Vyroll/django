from django.conf.urls import url, include
from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter

from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework.schemas import get_schema_view

# app_name = 'api' # can use because of DRF reverse implementation

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('Question', views.QuestionViewSet)
router.register('Choice', views.ChoiceViewSet)

schema_view = get_schema_view(title='Pastebin API')

urlpatterns = [
    path('schema/', schema_view),
    path('', include(router.urls)),
]
