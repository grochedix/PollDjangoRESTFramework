from django.contrib.auth.models import User
from .models import Question, Answer
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email"]


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    subanswers = RecursiveField(required=False, allow_null=True, many=True)

    class Meta:
        model = Answer
        fields = ["id", "text", "subanswers"]
        read_only_fields = ["id"]

    def validate(self, data):
        if bool(data["question"]) == bool(data["subanswers"]):
            raise serializers.ValidationError(
                "Either an answer to question, either a subanswer."
            )
        return data


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["text", "author", "answers"]
        read_only_fields = ["author"]


class AnswerListSerializer(serializers.HyperlinkedModelSerializer):
    subanswers = RecursiveField(required=False, allow_null=True, many=True)

    class Meta:
        model = Answer
        fields = ["id", "text", "question", "subanswers"]

    def validate(self, data):
        if bool(data["question"]) == bool(data["subanswers"]):
            raise serializers.ValidationError(
                "Either an answer to question, either a subanswer."
            )
        return data


class QuestionListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ["url", "text", "author"]
        read_only_fields = ["author", "url"]
