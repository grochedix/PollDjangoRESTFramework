from django.contrib.auth.models import User
from .models import Question, Answer
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "text"]
        read_only_fields = ["id"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["text", "author", "answers"]
        read_only_fields = ["author"]


class AnswerListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "text", "question"]


class QuestionListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ["url", "text", "author"]
        read_only_fields = ["author", "url"]
