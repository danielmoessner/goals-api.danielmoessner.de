from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from apps.users.serializers import CreateUserSerializer, ChangePasswordSerializer
from apps.users.models import CustomUser
from django.shortcuts import redirect
from rest_framework import generics, status
from django.views import generic


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
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SettingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'users/users_settings.j2'


class SignUpView(generic.TemplateView):
    template_name = 'users/users_sign_up.j2'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:redirect', permanent=False)
        return super(SignUpView, self).get(self, request, *args, **kwargs)


class SignInView(generic.TemplateView):
    template_name = 'users/users_sign_in.j2'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:redirect', permanent=False)
        return super(SignInView, self).get(self, request, *args, **kwargs)
