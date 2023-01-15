import requests
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Photo


# photo URL로 접근시 기능을 수행하는 view
class PhotoDetail(APIView):
    # 로그인 된 유저에 한해 기능 수행을 가능하게 함
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)
        if photo.sale.owner != request.user:
            raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_200_OK)


class GetUploadURL(APIView):
    # 사진 업로드시 지정된 url로 토큰을 post하고 데이터를 전송받음.
    def post(self, request):
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v2/direct_upload"
        one_time_url = requests.post(
            url,
            headers={"Authorization": f"Bearer {settings.CF_TOKEN}"},
        )
        one_time_url = one_time_url.json()
        result = one_time_url.get("result")
        return Response({"result": result})
