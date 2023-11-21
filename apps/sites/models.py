from django.contrib.gis.db.models import PointField
from django.db import models

from apps.locations.models import City
from apps.users.models import User
from apps.utils.models import BaseModel


class Site(BaseModel):
    title = models.CharField(max_length=255, default="unknown_title")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    base_site = models.ForeignKey("BaseSite", on_delete=models.CASCADE)
    overview = models.TextField()
    language = models.CharField(max_length=3)
    source = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)
    tags = models.ManyToManyField("SiteTag", related_name="tags")

    def __str__(self):
        return f"{self.base_site.city}: {self.base_site}"


class BaseSite(BaseModel):
    title = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    location = PointField(null=False, blank=False)

    def __str__(self):
        return f"{self.title}"


class SiteImage(BaseModel):
    base_site = models.ForeignKey(BaseSite, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/site_images/")
    thumbnail = models.ImageField(upload_to="media/site_thumbnails/")
    source = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.base_site.title}"


class SiteTag(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class SiteAudio(BaseModel):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    url = models.FileField(upload_to="media/site_audio/")
    duration = models.PositiveIntegerField()
    language = models.CharField(max_length=3)
    source = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.url}"
