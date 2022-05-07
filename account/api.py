from rest_framework.views import APIView

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
