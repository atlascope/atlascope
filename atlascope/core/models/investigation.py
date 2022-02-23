from typing import List
from uuid import uuid4

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import assign_perm, get_users_with_perms, remove_perm
from rest_framework import serializers


class Investigation(TimeStampedModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=5000, blank=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    datasets = models.ManyToManyField('Dataset', related_name='contexts')
    notes = models.TextField(max_length=5000, blank=True)

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


class InvestigationSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_owner')

    def get_owner(self, obj):
        return obj.owner.username or None

    class Meta:
        model = Investigation
        fields = ('id', 'name', 'description', 'owner')


class InvestigationDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_owner')
    investigators = serializers.SerializerMethodField('get_investigators')
    observers = serializers.SerializerMethodField('get_observers')

    def get_owner(self, obj):
        return obj.owner.username or None

    def get_investigators(self, obj) -> List[str]:
        return [
            user.username
            for user in get_users_with_perms(obj, only_with_perms_in=['change_investigation'])
        ]

    def get_observers(self, obj) -> List[str]:
        return [
            user.username
            for user in get_users_with_perms(obj, only_with_perms_in=['view_investigation'])
        ]

    class Meta:
        model = Investigation
        fields = [
            'id',
            'name',
            'description',
            'owner',
            'investigators',
            'observers',
            'datasets',
            'pins',
            'notes',
            'created',
            'modified',
        ]


@admin.register(Investigation)
class InvestigationAdmin(GuardedModelAdmin):
    list_display = ('name', 'owner')
    list_filter = ('created', 'modified', 'owner')
