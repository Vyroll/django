from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('testForm/<int:pk>/', views.TestFormView.as_view(), name='testForm'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('accounts/logout/', views.logoutView, name='logout'),
    path('accounts/register/', views.RegisterView, name='register'),
    path('creategrouppermissions/', 
        views.CreateGroupPermissions, 
        name='creategrouppermissions'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('gettoken/', views.GetTokenView, name='gettoken'),
]