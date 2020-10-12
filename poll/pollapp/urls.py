from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path("question/", views.QuestionListView.as_view()),
    path("question/<pk>/", views.QuestionView.as_view(), name="question-detail"),
    path("question/<pk>/answer/", views.QuestionAnswersListView.as_view()),
    path("answer/", views.AnswerListView.as_view()),
    path("answer/<pk>/", views.AnswerView.as_view(), name="answer-detail"),
]
