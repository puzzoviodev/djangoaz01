from medicSearch.models import *
class Rating(models.Model):
    user_rated = models.ForeignKey(User, related_name='rated_by',
        on_delete=models.CASCADE)
    user_rating = models.ForeignKey(User, related_name='rating_by',
        on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    opinion = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """Return a string representation of the Rating model."""
        return '{} avaliou {} com nota {}'.format(
            self.user_rated, self.user_rating, self.value)