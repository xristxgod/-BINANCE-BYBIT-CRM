from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import get_authorization_header

from core.login.models import AuthToken


class ApiTokenAuthentication(TokenAuthentication):
    model = AuthToken

    def get_token_from_header(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return token

    def get_token_from_cookie(self, request):
        if settings.TOKEN_COOKIE_NAME not in request.COOKIES:
            return None

        try:
            token = request.COOKIES[settings.TOKEN_COOKIE_NAME]
        except UnicodeError:
            msg = _('Invalid token cookie. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return token

    def authenticate(self, request):
        header_token = cookie_token = None
        try:
            header_token = self.get_token_from_header(request)
        except exceptions.AuthenticationFailed as e:
            raise

        if not header_token:
            return None
        if header_token and cookie_token and header_token != cookie_token:
            msg = _('Header and cookie tokens are differ.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(header_token or cookie_token)

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        customer = token.customer

        if not customer or not customer.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        if token.is_expired:
            raise exceptions.AuthenticationFailed(_('Token has expired.'))

        return customer, token
