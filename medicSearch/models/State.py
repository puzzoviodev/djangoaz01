
from medicSearch.models import *


class State(models.Model):
    """State model."""

    name = models.CharField(null=False, max_length=20)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the State model."""
        return '{}'.format(self.name)