from django.shortcuts import get_object_or_404
from django.utils.functional import wraps
from guardian.shortcuts import get_perms
from rest_framework import status
from rest_framework.response import Response

from atlascope.core.models import Investigation


def has_edit_perm(user, obj):
    user_perms_on_obj = get_perms(user, obj)
    return any(perm in user_perms_on_obj for perm in type(obj).get_write_permission_groups()) or (
        hasattr(obj, 'owner') and user == obj.owner
    )


def has_read_perm(user, obj):
    user_perms_on_obj = get_perms(user, obj)
    return any(perm in user_perms_on_obj for perm in type(obj).get_read_permission_groups()) or (
        hasattr(obj, 'owner') and user == obj.owner
    )


def object_permission_required(
    model=Investigation, edit_access=False, superuser_access=False, **decorator_kwargs
):
    def decorator(view_func):
        def _wrapped_view(viewset, *args, **wrapped_view_kwargs):
            if decorator_kwargs:
                lookup_dict = {
                    key: wrapped_view_kwargs[value] for key, value in decorator_kwargs.items()
                }
            else:
                lookup_dict = {'pk': wrapped_view_kwargs['pk']}
            obj = get_object_or_404(model, **lookup_dict)

            user = viewset.request.user
            edit_perm = has_edit_perm(user, obj)
            read_perm = has_read_perm(user, obj)
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
