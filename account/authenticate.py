from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions

def enforce_csrf(request):
    """
    Enforce CSRF validation.
    """
    csrf_token = request.COOKIES.get('csrftoken')  # Adjust the cookie name if needed

    if not csrf_token:
        raise exceptions.PermissionDenied('CSRF Failed: Missing CSRF token in cookie')

    def dummy_get_response(request):  # pragma: no cover
        return None

    check = CSRFCheck(dummy_get_response)
    # Include CSRF token in the headers for the CSRFCheck
    request.META['HTTP_X_CSRFTOKEN'] = csrf_token

    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)

class CustomAuthentication(JWTAuthentication):
    """Custom authentication class"""
    def authenticate(self, request):
        header = self.get_header(request)
        print("Aaaaaaaaaaa")
        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        enforce_csrf(request)
        return self.get_user(validated_token), validated_token