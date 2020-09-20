from rest_framework import serializers
from apps.users.models import CustomUser


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print('already here')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='users:customuser-detail')
    id = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        # fields = '__all__'
        exclude = ['user_permissions', 'password', 'is_staff', 'is_superuser', 'last_login', 'is_active', 'date_joined',
                   'groups', 'first_name', 'last_name']