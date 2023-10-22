from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import serializers, permissions, status

from account.serializers import get_serialized_user
from account.models import User
from common.utils.api import get_api_response


class UserAPIView(APIView):
    """
    User API View
    """
    def get(self, request):
        """
        Return serialized payload of authenticated user
        Args:
            request:

        Returns:
            DjangoRest Response:
        """
        return get_api_response(get_serialized_user(request.user))

    def post(self, request):
        data = request.user
        user = User.objects.create(**data)
        return get_api_response(get_serialized_user(user))


class UserTokenAPIView(ObtainAuthToken):

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=False)

        try:
            user = serializer.validated_data['user']
        except KeyError as e:
            user = None

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return get_api_response({
                    'token': token.key,
                    "username": user.username,
                    "name": user.get_full_name()
                })
        else:
            return get_api_response({
                    "message": "Wrong email or password"
            }, status=status.HTTP_401_UNAUTHORIZED)
