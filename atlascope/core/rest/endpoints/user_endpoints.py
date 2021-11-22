from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from atlascope.core.rest.additional_serializers import UserSerializer


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    model = User
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, pagination_class=None)
    def me(self, request):
        """Return the currently logged in user's information."""
        if request.user.is_anonymous:
            return Response(status=204)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
