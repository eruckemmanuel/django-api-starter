import logging

from rest_framework.response import Response
from rest_framework import status as rest_status


logger = logging.getLogger(__name__)

def get_api_response(data, message="Ok", status=rest_status.HTTP_200_OK):
    context = {
        "data": data,
        "message": message
    }

    return Response(context, status=status)
