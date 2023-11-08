from django.db import models

from apps.utils.models import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name}"


class City(BaseModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="media/city_images/")

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.name}"
