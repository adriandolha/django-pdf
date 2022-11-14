from django.contrib.auth.models import User, Group, Permission
from django.http import HttpResponse

from django_pdf import settings
from django_pdf.logger import LOGGER
from django.shortcuts import redirect


def requires_permission(permissions: list):
    def requires_permission_decorator(function):
        def wrapper(*args, **kwargs):
            request = args[0]
            LOGGER.info(f'Authorization...')
            if not request.user.is_authenticated:
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

            if permissions and len(permissions) > 0 and (
                    not all([request.user.has_perm(perm) for perm in permissions])):
                return HttpResponse('Forbidden', status=403)
            _result = function(*args, **kwargs)
            return _result

        wrapper.__name__ = function.__name__
        wrapper.__doc__ = function.__doc__
        return wrapper

    return requires_permission_decorator
