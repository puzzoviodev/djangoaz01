from medicSearch.models import *
class Speciality(models.Model):
    """
    Speciality model
    """
    name = models.CharField(null=False, max_length=100)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return a string representation of the Specialty model
        """
        return '{}'.format(self.name)

