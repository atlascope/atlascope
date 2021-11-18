from atlascope.core.models import Investigation
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from guardian.shortcuts import get_perms
from rest_framework import status
from django.utils.functional import wraps


def has_edit_perm(user, investigation):
    user_perms_on_investigation = get_perms(user, investigation)
    return (
        any(
            perm in user_perms_on_investigation
            for perm in Investigation.get_write_permission_groups()
        )
        or user == investigation.owner
    )


def has_read_perm(user, investigation):
    user_perms_on_investigation = get_perms(user, investigation)
    return (
        any(
            perm in user_perms_on_investigation
            for perm in Investigation.get_read_permission_groups()
        )
        or user == investigation.owner
    )


def investigation_permission_required(
    edit_access=False, superuser_access=False, **decorator_kwargs
):
    def decorator(view_func):
        def _wrapped_view(viewset, *args, **wrapped_view_kwargs):
            if decorator_kwargs:
                lookup_dict = {
                    key: wrapped_view_kwargs[value] for key, value in decorator_kwargs.items()
                }
            else:
                lookup_dict = {'pk': wrapped_view_kwargs['pk']}
            investigation = get_object_or_404(Investigation, **lookup_dict)

            user = viewset.request.user
            edit_perm = has_edit_perm(user, investigation)
            read_perm = has_read_perm(user, investigation)
            error_response = Response(status=status.HTTP_401_UNAUTHORIZED)

            if (
                (superuser_access and not user.is_superuser)
                or (edit_access and not edit_perm)
                or not read_perm
            ):
                return error_response

            return view_func(viewset, *args, **wrapped_view_kwargs)

        return wraps(view_func)(_wrapped_view)

    return decorator
