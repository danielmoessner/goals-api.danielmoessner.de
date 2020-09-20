from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework import serializers


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label="E-Mail")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer


obtain_auth_token = CustomObtainAuthToken.as_view()
