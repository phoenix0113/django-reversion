from django.db import models
import reversion
from reversion.models import Revision


@reversion.register()
class TestModel(models.Model):

    name = models.CharField(
        max_length=191,
        default="v1",
    )


class TestModelUnregistered(models.Model):

    name = models.CharField(
        max_length=191,
        default="v1",
    )


class TestMeta(models.Model):

    revision = models.ForeignKey(
        Revision,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=191,
    )
