from uuid import uuid4

from django.contrib import admin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django_extensions.db.models import TimeStampedModel
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import assign_perm, get_users_with_perms, remove_perm
from rest_framework import serializers

from atlascope.core.models import ConnectionsMap, ContextMap


class Investigation(TimeStampedModel, models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    context_map = models.OneToOneField('ContextMap', on_delete=models.PROTECT, editable=False)
    connections_map = models.OneToOneField(
        'ConnectionsMap', on_delete=models.PROTECT, editable=False
    )

    def save(self, *args, **kwargs):
        # enforce creation of maps for this investigation
        try:
            self.context_map
        except ObjectDoesNotExist:
            new_context_map = ContextMap()
            new_context_map.save()
            self.context_map = new_context_map
        try:
            self.connections_map
        except ObjectDoesNotExist:
            new_connections_map = ConnectionsMap()
            new_connections_map.save()
            self.connections_map = new_connections_map
        super().save(*args, **kwargs)

    def get_read_permission_groups():
        return ['view_investigation', 'change_investigation']

    def get_write_permission_groups():
        return ['change_investigation']

    def update_group(self, group_name, user_list):
        if group_name not in Investigation.get_read_permission_groups():
            raise ValueError(f'Error: {group_name} is not a valid group on this Project.')

        old_list = get_users_with_perms(self, only_with_perms_in=[group_name])
        for previously_permitted_user in old_list:
            if previously_permitted_user.username not in user_list:
                remove_perm(group_name, previously_permitted_user, self)

        for username in user_list:
            new_permitted_user = User.objects.get(username=username)
            if new_permitted_user not in old_list:
                assign_perm(group_name, new_permitted_user, self)


class InvestigationSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')

    class Meta:
        model = Investigation
        exclude = ('context_map', 'connections_map')


class InvestigationDetailSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    investigators = serializers.SerializerMethodField('get_investigators')
    observers = serializers.SerializerMethodField('get_observers')

    def get_investigators(self, obj):
        return [
            user.username
            for user in get_users_with_perms(
                obj, only_with_perms_in=Investigation.get_write_permission_groups()
            )
        ]

    def get_observers(self, obj):
        return [user.username for user in get_users_with_perms(obj)]

    class Meta:
        model = Investigation
        exclude = ('context_map', 'connections_map')


@admin.register(Investigation)
class InvestigationAdmin(GuardedModelAdmin):
    list_display = ('name', 'owner')
    list_filter = ('created', 'modified', 'owner')
