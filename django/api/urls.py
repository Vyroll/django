from django.conf.urls import url, include
from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter

from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework.schemas import get_schema_view

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# app_name = 'api' # can't use because of DRF reverse implementation

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('Question', views.QuestionViewSet)
router.register('Choice', views.ChoiceViewSet)

schema_view = get_schema_view(title='Pastebin API')

urlpatterns = [
    path('', include(router.urls)),
    path('schema/', schema_view),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]