from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import ValidationError, NotAuthenticated, PermissionDenied, NotFound
from rest_framework import status

def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        return Response({
            "success": False,
            "message": "An unexpected error occurred.",
            "error_code": "INTERNAL_SERVER_ERROR",
            "errors": {}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    error_code = "ERROR"
    message = str(exc.detail) if hasattr(exc, 'detail') else str(exc)
    errors = {}

    if isinstance(exc, ValidationError):
        error_code = "VALIDATION_ERROR"
        message = "Validation failed."
        errors = exc.detail

    elif isinstance(exc, NotAuthenticated):
        error_code = "AUTHENTICATION_ERROR"

    elif isinstance(exc, PermissionDenied):
        error_code = "PERMISSION_DENIED"

    elif isinstance(exc, NotFound):
        error_code = "NOT_FOUND"

    return Response({
        "success": False,
        "message": message,
        "error_code": error_code,
        "errors": errors
    }, status=response.status_code)