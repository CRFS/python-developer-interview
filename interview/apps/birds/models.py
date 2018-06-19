from django.db import models
from interview.apps.nodes.models import Node


class Species(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name", "id",)


class Bird(models.Model):

    timestamp = models.DateTimeField()

    name = models.CharField(
        max_length=255,
    )

    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
    )

    node = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-timestamp", "-id",)
