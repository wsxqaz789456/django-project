from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Board, Comment
from .serializers import BoardSerializer, CommentSerializer

# 특정 url에 대하여 작성된 serializer를 통한 검증과 데이터 입출력을 나타내는 view작성


class Boards(APIView):

    """전체 게시글에 대한 get, post method 작성"""

    # 인증된 유저만 post method가 가능하며 인증이 되지 않은 유저의 경우 read만 가능.
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

    """특정 게시글에 대한 get, put, delete method 작성"""

    permission_classes = [IsAuthenticatedOrReadOnly]

    # 특정한 pk의 게시글을 불러오는 method
    def get_object(self, pk):
        try:
            return Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise NotFound

    # 게시글을 get method를 통해 불러올 경우 조회수 1 증가
    def get(self, request, pk):
        board = self.get_object(pk)
        board.views = board.views + 1
        board.save()
        serializer = BoardSerializer(board)

        return Response(serializer.data)

    # 게시글의 작성자와 로그인 유저의 일치여부를 확인하며 게시글 작성시 http code 200, 실패시 403전달
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
            return Response(
                BoardSerializer(updated_board).data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_403_FORBIDDEN,
            )

    def delete(self, request, pk):
        board = self.get_object(pk)
        if board.author != request.user:
            raise PermissionDenied(status=status.HTTP_403_FORBIDDEN)
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BoardComments(APIView):

    """특정 pk의 게시글에 작성된 댓글들을 불러오거나 작성"""

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
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


class Comments(APIView):

    """작성된 게시글을 delete"""

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        comment = self.get_object(pk)
        if comment.author != request.user:
            raise PermissionDenied(status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_200_OK)
