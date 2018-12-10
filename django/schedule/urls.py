from django.urls import path
from schedule.views import LandingView, ScheduleList
# from . import views

# from myapp.views import MyView

# app_name = 'schedule'

urlpatterns = [
    # path('', LandingView.as_view(), name='LandingView'),
    path('', ScheduleList.as_view(), name='ScheduleList'),
]