from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("question/", views.QuestionListView.as_view()),
    path("question/<pk>/", views.QuestionView.as_view(), name="question-detail"),
    path("question/<pk>/answer/", views.AnswerListView.as_view()),
    path("answer/<pk>/", views.AnswerView.as_view(), name="answer-detail"),
]
