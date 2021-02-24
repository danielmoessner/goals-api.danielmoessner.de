from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from apps.users.serializers import UserSerializer, ChangePasswordSerializer, CreateUserSerializer, AuthTokenSerializer
from apps.users.models import CustomUser
from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.models import Token


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.none()

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.request.user.pk)

    def create(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['post'], detail=False)
    def auth_token(self, request):
        serializer = AuthTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    @action(methods=['post'], detail=False)
    @permission_classes([permissions.IsAuthenticated])
    def change_password(self, request):
        user = self.request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # check new passwords are the same
            if not serializer.data.get("new_password") == serializer.data.get('password_confirm'):
                return Response({'password_confirm': ['Has to be the same as new password.']},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
