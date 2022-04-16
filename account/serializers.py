from rest_framework import serializers

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email", "last_login"]


def get_serialized_user(user, many=False):
    return UserSerializer(user).data
