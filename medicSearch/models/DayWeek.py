from medicSearch.models import *

class DayWeek(models.Model):
    """Model for DayWeek table"""
    name = models.CharField(null=False, max_length=20)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the DayWeek model"""
        return '{}'.format(self.name)