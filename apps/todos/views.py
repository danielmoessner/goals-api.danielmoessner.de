import json

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class APIStatus(APIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['options', 'get']

    def get(self, request):
        data = {
            "status": self.request.user.to_dos.count() + self.request.user.to_dos.filter(activate=None).count()
        }
        return Response(data)

