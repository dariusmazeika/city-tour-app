from django.db import models

from apps.sites.models import Site
from apps.users.models import User
from apps.utils.models import BaseModel


class TourSite(BaseModel):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    tour = models.ForeignKey("Tour", on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.site} {self.tour} {self.order}"


class Tour(BaseModel):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_tours")
    language = models.CharField(max_length=3)
    overview = models.TextField()
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    source = models.CharField(max_length=255)
    is_audio = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    sites = models.ManyToManyField(Site, through=TourSite)

    def __str__(self):
        return f"{self.title}"


class UserTour(BaseModel):
    STARTED = "Started"
    FINISHED = "Finished"
    NEW = "New"
    STATUSES = [
        (STARTED, "Started"),
        (FINISHED, "Finished"),
        (NEW, "New"),
    ]
    tour = models.ForeignKey(Tour, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField()
    status = models.CharField(max_length=8, choices=STATUSES, default=NEW)

    def __str__(self):
        return f"{self.tour}"
