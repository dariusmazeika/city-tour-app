from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.db import models

from apps.utils.models import BaseModel


class Review(BaseModel):
    text = models.TextField(default="", blank=True, validators=[MinLengthValidator(20)])
    rating = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )
    tour = models.ForeignKey("tours.Tour", on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reviews")
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reviewer}'s review [{self.rating}]"

    def save(self, *args, **kwargs):
        if not self.text:
            self.is_approved = True
        super().save(*args, **kwargs)
