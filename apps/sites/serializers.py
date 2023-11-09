from rest_framework import serializers

from apps.sites.models import Site


class SiteSerializer(serializers.ModelSerializer):
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
