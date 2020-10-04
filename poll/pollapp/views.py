from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    QuestionSerializer,
    QuestionListSerializer,
    AnswerSerializer,
)
from .models import Question, Answer, Vote


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionListView(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        try:
            return Response(
                QuestionListSerializer(
                    Question.objects.all(), many=True, context={"request": request}
                ).data
            )
        except Question.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        serializer = QuestionListSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        question = self.get_object(pk)
        if request.user == question.author:
            serializer = QuestionSerializer(question, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            QuestionSerializer(question).data, status=status.HTTP_403_FORBIDDEN
        )

    def delete(self, request, pk, format=None):
        question = self.get_object(pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerListView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_question(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        question = self.get_question(pk)
        answer = Answer.objects.filter(question=question)
        serializer = AnswerSerializer(answer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        question = self.get_question(pk)
        if question.author == request.user:
            serializer = AnswerSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save(question=question)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)


class AnswerView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        answer = self.get_object(pk)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        answer = self.get_object(pk)
        if not (Vote.objects.filter(user=request.user, answer=answer).exists()):
            vote = Vote(user=request.user, answer=answer)
            vote.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        answer = self.get_object(pk)
        if request.user == answer.question.author:
            serializer = AnswerSerializer(answer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            AnswerSerializer(question).data, status=status.HTTP_403_FORBIDDEN
        )

    def delete(self, request, pk, format=None):
        answer = self.get_object(pk)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
