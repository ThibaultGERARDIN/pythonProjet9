from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Ticket(models.Model):

    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")
    time_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Set the author to the current user before saving
        if not self.pk:  # Check if it's a new instance
            self.user = kwargs.pop("user", None)
        super().save(*args, **kwargs)


class Review(models.Model):

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="Note"
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    headline = models.CharField(max_length=128, verbose_name="Titre")
    body = models.TextField(max_length=8192, blank=True, verbose_name="Commentaire")
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="followed_by")

    class Meta:
        unique_together = ("user", "followed_user")
