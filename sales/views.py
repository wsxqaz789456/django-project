from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .serializers import (
    SalesTitleSerializers,
    SalesSerializers,
    QuestionSerializer,
)
from .models import Sales, Question

from categories.models import Category
from photos.serializers import PhotoSerializer


class Sale(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_sale = Sales.objects.all()
        serializer = SalesTitleSerializers(
            all_sale,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = SalesSerializers(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError
            try:
                category = Category.objects.get(pk=category_pk)
            except Category.DoesNotExist:
                raise ParseError
            sale = serializer.save(
                owner=request.user,
                category=category,
            )
            serializer = SalesSerializers(sale)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class SaleDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Sales.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        sale = self.get_object(pk)
        serializer = SalesSerializers(sale)
        return Response(serializer.data)

    def put(self, request, pk):
        sale = self.get_object(pk)
        if sale.owner != request.user:
            raise PermissionDenied
        serializer = SalesSerializers(
            sale,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            if "category" in request.data:
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("카테고리가 없습니다")
                try:
                    category = Category.objects.get(pk=category_pk)
                except Category.DoesNotExist:
                    raise ParseError("존재하지 않는 카테고리 입니다.")
                sale = serializer.save(category=category)
                serializer = SalesSerializers(sale)
                return Response(serializer.data)
            sale = serializer.save()
            serializer = SalesSerializers(sale)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        sale = self.get_object(pk)
        if sale.owner != request.user:
            raise PermissionDenied
        sale.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)


class Questsions(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Sales.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        sale = self.get_object(pk)
        questions = sale.questions.all()
        serializer = QuestionSerializer(
            questions,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            parent_pk = request.data.get("parent")
            if parent_pk:
                parent = Question.objects.get(pk=parent_pk)
                if parent.parent_id != None:
                    raise ParseError("답변에 답변을 허용하지 않습니다.")
            serializer.save(
                author=request.user,
                product=self.get_object(pk),
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class QuestionDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_sale(self, pk):
        try:
            return Sales.objects.get(pk=pk)
        except Sales.DoesNotExist:
            raise NotFound

    def get_question(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise NotFound

    def get(self, request, pk, q_pk):
        sale = self.get_sale(pk)
        question = self.get_question(q_pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, pk, q_pk):
        sale = self.get_sale(pk)
        question = sale.questions.get(pk=q_pk)

        if question.author != request.user:
            raise PermissionDenied
        serializer = QuestionSerializer(
            question,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk, q_pk):
        sale = self.get_sale(pk)
        question = sale.questions.get(pk=q_pk)
        if question.author != request.user or sale.owner != request.user:
            raise PermissionDenied
        question.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)


""" class Answer(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Sales.objects.get(pk=pk)
        except:
            return NotFound

    def get(self, request, pk, q_pk, a_pk):
        sale = self.get_object(pk)
        question = sale.questions.get(pk=q_pk)
        answer = question.answers.get(pk=a_pk)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)

    def put(self, request, pk, q_pk, a_pk):
        sale = self.get_object(pk)
        question = sale.questions.get(pk=q_pk)
        answer = question.answers.get(pk=a_pk)
        if answer.author != request.user:
            raise PermissionDenied
        serialzier = AnswerSerializer(answer, data=request.data, partial=True)
        if serialzier.is_valid():
            new_answer = serialzier.save()
            return Response(AnswerSerializer(new_answer).data)
        else:
            return Response(serialzier.errors)

    def delete(self, request, pk, q_pk, a_pk):
        sale = self.get_object(pk)
        question = sale.questions.get(pk=q_pk)
        answer = question.answers.get(pk=a_pk)
        if answer.author != request.user:
            raise PermissionDenied
        answer.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)
 """


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Sales.objects.get(pk=pk)
        except Sales.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        sale = self.get_object(pk)
        if request.user != sale.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(sale=sale)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
