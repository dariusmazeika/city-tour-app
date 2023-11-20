from rest_framework import serializers

from apps.sites.models import BaseSite, Site, SiteImage


class CreateBaseSiteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteImage
        fields = (
            "image",
            "thumbnail",
            "source",
        )


class CreateSiteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteImage
        fields = (
            "id",
            "base_site",
            "image",
            "thumbnail",
            "source",
        )


class BaseSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseSite
        fields = (
            "id",
            "created_at",
            "updated_at",
            "city",
            "longitude",
            "latitude",
            "title",
        )


class CreateBaseSiteSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    thumbnail = serializers.ImageField(required=False)
    image_source = serializers.CharField(required=False, max_length=255, allow_blank=False)

    class Meta:
        model = BaseSite
        fields = (
            "id",
            "city",
            "longitude",
            "latitude",
            "title",
            "image",
            "thumbnail",
            "image_source",
        )

    def create(self, validated_data):
        image_data = validated_data.pop("image", None)
        thumbnail_data = validated_data.pop("thumbnail", None)
        image_source_data = validated_data.pop("image_source", None)

        if image_data or image_source_data or thumbnail_data:
            site_image_data = {
                "image": image_data,
                "thumbnail": thumbnail_data,
                "source": image_source_data,
            }
            image_serializer = CreateBaseSiteImageSerializer(data=site_image_data)
            image_serializer.is_valid(raise_exception=True)

            base_site = super().create(validated_data)
            SiteImage.objects.create(base_site=base_site, **site_image_data)

        else:
            base_site = super().create(validated_data)

        return base_site


class SiteSerializer(serializers.ModelSerializer):
    base_site = BaseSiteSerializer(read_only=True)

    class Meta:
        model = Site
        fields = (
            "id",
            "created_at",
            "updated_at",
            "title",
            "overview",
            "language",
            "source",
            "is_approved",
            "author",
            "base_site",
        )
        read_only_fields = (
            "created_at",
            "updated_at",
            "title",
            "overview",
            "language",
            "source",
            "is_approved",
            "author",
            "base_site",
        )


class CreateSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = (
            "id",
            "title",
            "overview",
            "language",
            "source",
            "base_site",
            "tags",
        )

    def create(self, validated_data):
        current_user = self.context["request"].user
        validated_data["author"] = current_user

        return super().create(validated_data)
