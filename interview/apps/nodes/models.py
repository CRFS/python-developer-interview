from django.db import models


class Node(models.Model):

    name = models.CharField(
        max_length=255,
    )

    ip_address = models.GenericIPAddressField()

    port = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            ("ip_address", "port",),
        )
        ordering = ("name", "id",)
