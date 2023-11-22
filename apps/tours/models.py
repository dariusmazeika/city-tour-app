from django.contrib.gis.db.models import MakeLine
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
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_tours")
    language = models.CharField(max_length=3)
    overview = models.TextField()
    source = models.CharField(max_length=255)
    is_audio = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_private = models.BooleanField(default=True)
    sites = models.ManyToManyField(Site, through=TourSite)
    finished_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title}"

    @property
    def distance(self) -> float:
        if self.sites.count() > 1:
            tour_route_line = (
                self.sites.order_by("toursite__order").aggregate(line=MakeLine("base_site__location")).get("line", None)
            )
            tour_route_line.transform(3035)
            return round(tour_route_line.length / 1000, 2)  # return length in km
        return 0


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
    status = models.CharField(max_length=8, choices=STATUSES, default=NEW)
    is_finished_once = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tour}"


class SharedPrivateTour(BaseModel):
    shared_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="shared_by_user", null=True)
    user_tour = models.OneToOneField(UserTour, on_delete=models.CASCADE, related_name="shared_private_tour")

    def __str__(self) -> str:
        return f"{self.shared_by} {self.user_tour}"
