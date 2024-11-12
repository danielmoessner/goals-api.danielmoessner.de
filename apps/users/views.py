from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users.models import CustomUser
from apps.users.serializers import ChangePasswordSerializer, CreateUserSerializer


class CreateUser(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # check new passwords are the same
            print(serializer.data.get("password_confirm"))
            if not serializer.data.get("new_password") == serializer.data.get(
                "password_confirm"
            ):
                return Response(
                    {"password_confirm": ["Has to be the same as new password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
