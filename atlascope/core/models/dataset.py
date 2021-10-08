from uuid import uuid4

from django.contrib import admin
from django.db import models


class Dataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    source_uri = models.CharField(max_length=3000, null=False, blank=False)
    # import_function
    # scale


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('id', 'source_uri')
