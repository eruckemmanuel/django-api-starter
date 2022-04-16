from rest_framework import serializers
from rest_framework import status


class RequestValidationError(serializers.ValidationError):
    status_code = status.HTTP_400_BAD_REQUEST


class EntityNotFoundError(serializers.ValidationError):
    status_code = status.HTTP_404_NOT_FOUND


class InternalServerError(serializers.ValidationError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class RequestUnAuthorizedError(serializers.ValidationError):
    status_code = status.HTTP_401_UNAUTHORIZED
