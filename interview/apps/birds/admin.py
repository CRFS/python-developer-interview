from django.contrib import admin
from interview.apps.birds.models import Species, Bird


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):

    search_fields = ("name",)

    list_display = ("name",)

    fieldsets = (
        (None, {
            "fields": (
                "name",
            ),
        }),
    )


@admin.register(Bird)
class BirdAdmin(admin.ModelAdmin):

    search_fields = ("name",)

    list_display = ("timestamp", "name", "species", "node",)

    list_filter = ("species", "node",)

    fieldsets = (
        (None, {
            "fields": (
                "timestamp",
                "name",
                "species",
                "node",
            ),
        }),
    )
