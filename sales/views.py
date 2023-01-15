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


# 특정 url에 대하여 작성된 serializer를 통한 검증과 데이터 입출력을 나타내는 view작성


class Sale(APIView):

    """판매 게시글에 대한 get, post method 작성"""

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

    """특정 게시글에 대한 get, put, delete method 작성"""

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Sales.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        sale = self.get_object(pk)
        serializer = SalesSerializers(
            sale,
            context={"request": request},
        )
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
            # put method 작성시 전달받은 데이터에 category항목이 없을 경우
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
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        sale = self.get_object(pk)
        if sale.owner != request.user:
            raise PermissionDenied
        sale.delete()
        return Response(status=status.HTTP_200_OK)


class Questsions(APIView):

    """특정 pk의 게시글에 대한 댓글 get, post method 작성"""

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
            # post method 실행시 parent 값을 전달받았을 경우
            # 해당 parent의 값이 null이 아닐 시에 댓글 작성을 제한
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
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk, q_pk):
        sale = self.get_sale(pk)
        question = sale.questions.get(pk=q_pk)
        if question.author != request.user or sale.owner != request.user:
            raise PermissionDenied
        question.delete()
        return Response(status=status.HTTP_200_OK)


class SalePhotos(APIView):

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
