from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Board, Comment
from .serializers import BoardSerializer, CommentSerializer


class Boards(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_boards = Board.objects.all()
        serializer = BoardSerializer(
            all_boards,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = BoardSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            new_board = serializer.save(
                author=request.user,
            )
            return Response(BoardSerializer(new_board).data)
        else:
            return Response(serializer.errors)


class BoardDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        serializer = BoardSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        board = self.get_object(pk)
        if board.author != request.user:
            raise PermissionDenied
        serializer = BoardSerializer(
            board,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_board = serializer.save()
            return Response(BoardSerializer(updated_board).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        board = self.get_object(pk)
        if board.author != request.user:
            raise PermissionDenied
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BoardComments(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        board = Board.objects.get(pk=pk)
        comments = board.comments.all()
        serializer = CommentSerializer(
            comments,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = CommentSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            new_comment = serializer.save(
                author=request.user,
                article=self.get_object(pk),
            )
            return Response(CommentSerializer(new_comment).data)
        else:
            return Response(serializer.errors)


class Comments(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        comment = self.get_object(pk)
        if comment.author != request.user:
            raise PermissionDenied
        comment.delete()
        return Response(status=status.HTTP_200_OK)
