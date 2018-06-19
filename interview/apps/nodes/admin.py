from django.contrib import admin
from interview.apps.nodes.models import Node


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):

    search_fields = ("name",)

    list_display = ("name", "ip_address", "port",)

    fieldsets = (
        (None, {
            "fields": (
                "name",
                ("ip_address", "port",),
            ),
        }),
    )
