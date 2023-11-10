from rest_framework import serializers

from apps.sites.models import BaseSite, Site


class BaseSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseSite
        fields = "__all__"


class SiteSerializer(serializers.ModelSerializer):
    base_site = BaseSiteSerializer()

    class Meta:
        model = Site
        fields = (
            "id",
            "created_at",
            "updated_at",
            "overview",
            "language",
            "source",
            "is_approved",
            "author",
            "base_site",
        )
