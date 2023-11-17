import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from model_bakery.baker import make
from PIL import Image
import pytest
from rest_framework import status

from apps.locations.models import City
from apps.sites.models import BaseSite, Site, SiteImage, SiteTag
from apps.utils.tests_query_counter import APIClientWithQueryCounter
from conf.settings_test import TEST_DIR


class TestCreateSite:
    def test_unauthenticated_client_cannot_create_site(self, client: APIClientWithQueryCounter):
        path = reverse("sites-list")
        response = client.post(path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()

    def test_create_site(self, authorized_client: APIClientWithQueryCounter):
        path = reverse("sites-list")
        base_site = make(BaseSite, id=1)
        site_tag_one = make(SiteTag, id=1)
        site_tag_two = make(SiteTag, id=2)

        site_data = {
            "overview": "string",
            "language": "str",
            "source": "string",
            "base_site": base_site.id,
            "tags": [
                site_tag_one.id,
                site_tag_two.id,
            ],
        }

        response = authorized_client.post(path, site_data, format="json", query_limit=8)

        assert response.status_code == status.HTTP_201_CREATED, response.json()

        assert Site.objects.count() == 1

        created_site = Site.objects.first()
        created_site_tags_ids = list(created_site.tags.values_list("id", flat=True))

        assert created_site.overview == site_data["overview"]
        assert created_site.language == site_data["language"]
        assert created_site.source == site_data["source"]
        assert created_site.base_site.id == site_data["base_site"]
        assert created_site_tags_ids == site_data["tags"]

    def test_create_site_without_data_returns_bad_request(self, authorized_client: APIClientWithQueryCounter):
        path = reverse("sites-list")

        response = authorized_client.post(path, {})

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()

        expected_error = {
            "overview": ["This field is required."],
            "language": ["This field is required."],
            "source": ["This field is required."],
            "base_site": ["This field is required."],
            "tags": ["This list may not be empty."],
        }

        assert response.json() == expected_error

    def test_create_site_with_invalid_tag_data(self, authorized_client: APIClientWithQueryCounter):
        path = reverse("sites-list")
        base_site = make(BaseSite, id=1)
        site_tag = make(SiteTag, id=1)

        invalid_tag_id = 100
        invalid_site_data = {
            "overview": "string",
            "language": "str",
            "source": "string",
            "base_site": base_site.id,
            "tags": [
                invalid_tag_id,
                site_tag.id,
            ],
        }

        response = authorized_client.post(path, invalid_site_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()

        assert Site.objects.count() == 0


class TestCreateBaseSite:
    def test_unauthenticated_client_cannot_create_base_site(self, client: APIClientWithQueryCounter):
        path = reverse("base-sites-list")
        response = client.post(path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()

    def test_create_base_site(self, authorized_client: APIClientWithQueryCounter):
        path = reverse("base-sites-list")
        city = make(City)

        base_site_data = {
            "city": city.id,
            "longitude": 5,
            "latitude": 5,
            "title": "title",
        }

        response = authorized_client.post(path, base_site_data, format="multipart")

        assert response.status_code == status.HTTP_201_CREATED, response.json()

        assert BaseSite.objects.count() == 1

        created_base_site = BaseSite.objects.first()
        assert created_base_site.city.id == base_site_data["city"]
        assert created_base_site.longitude == base_site_data["longitude"]
        assert created_base_site.latitude == base_site_data["latitude"]
        assert created_base_site.title == base_site_data["title"]

    def test_create_base_site_without_data_returns_bad_request(self, authorized_client: APIClientWithQueryCounter):
        path = reverse("base-sites-list")

        response = authorized_client.post(path, {})

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()

        expected_error = {
            "city": ["This field is required."],
            "longitude": ["This field is required."],
            "latitude": ["This field is required."],
            "title": ["This field is required."],
        }

        assert response.json() == expected_error

    def test_create_base_site_with_invalid_city_data(self, authorized_client: APIClientWithQueryCounter):
        path = reverse("base-sites-list")

        invalid_city_id = 100
        invalid_base_site_data = {
            "city": invalid_city_id,
            "longitude": 5,
            "latitude": 5,
            "title": "title",
        }
        response = authorized_client.post(path, invalid_base_site_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()

        assert BaseSite.objects.count() == 0

    @pytest.mark.usefixtures("cleanup_media_folder")
    def test_create_base_site_with_image(self, authorized_client: APIClientWithQueryCounter):
        with override_settings(MEDIA_ROOT=(TEST_DIR + "/media")):
            path = reverse("base-sites-list")
            city = make(City)

            image_file = self._create_test_image()
            thumbnail_file = self._create_test_image()

            base_site_and_image_data = {
                "city": city.id,
                "longitude": 5,
                "latitude": 5,
                "title": "title",
                "image": image_file,
                "thumbnail": thumbnail_file,
                "image_source": "image_source",
            }

            response = authorized_client.post(path, base_site_and_image_data, format="multipart")

            assert response.status_code == status.HTTP_201_CREATED, response.json()

            assert BaseSite.objects.count() == 1
            assert SiteImage.objects.count() == 1

            created_base_site = BaseSite.objects.first()
            assert created_base_site.city.id == base_site_and_image_data["city"]
            assert created_base_site.longitude == base_site_and_image_data["longitude"]
            assert created_base_site.latitude == base_site_and_image_data["latitude"]
            assert created_base_site.title == base_site_and_image_data["title"]

            created_site_image = SiteImage.objects.first()
            assert created_site_image.base_site == created_base_site
            assert created_site_image.source == base_site_and_image_data["image_source"]

            image_file.seek(0)
            thumbnail_file.seek(0)
            assert created_site_image.image.read() == image_file.read()
            assert created_site_image.thumbnail.read() == thumbnail_file.read()

    def _create_test_image(self) -> SimpleUploadedFile:
        image = Image.new("RGB", (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix=".png")
        image.save(tmp_file)
        tmp_file.seek(0)
        return SimpleUploadedFile("test_image.png", tmp_file.read(), content_type="image/png")


class TestUploadImageViewSet:
    def test_unauthenticated_client_cannot_upload_image(self, client: APIClientWithQueryCounter):
        path = reverse("images-list")
        response = client.post(path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()

    @pytest.mark.usefixtures("cleanup_media_folder")
    def test_upload_image_with_valid_data(self, authorized_client: APIClientWithQueryCounter):
        with override_settings(MEDIA_ROOT=(TEST_DIR + "/media")):
            base_site = make(BaseSite)
            path = reverse("images-list")

            image_file = self._create_test_image()
            thumbnail_file = self._create_test_image()

            image_data = {
                "base_site": base_site.id,
                "image": image_file,
                "thumbnail": thumbnail_file,
                "source": "source",
            }

            response = authorized_client.post(path, image_data, format="multipart")

            assert response.status_code == status.HTTP_201_CREATED, response.json()

            assert SiteImage.objects.count() == 1

            created_site_image = SiteImage.objects.first()
            assert created_site_image.base_site.id == image_data["base_site"]
            assert created_site_image.source == image_data["source"]

            image_file.seek(0)
            thumbnail_file.seek(0)
            assert created_site_image.image.read() == image_file.read()
            assert created_site_image.thumbnail.read() == thumbnail_file.read()

    def test_upload_image_without_data_returns_bad_request(self, authorized_client: APIClientWithQueryCounter):
        path = reverse("images-list")

        response = authorized_client.post(path, {})

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()

        expected_error = {
            "base_site": ["This field is required."],
            "image": ["No file was submitted."],
            "thumbnail": ["No file was submitted."],
            "source": ["This field is required."],
        }

        assert response.json() == expected_error

    def test_upload_non_image_file(self, authorized_client: APIClientWithQueryCounter):
        base_site = make(BaseSite)
        path = reverse("images-list")

        txt_content = b"Hello, this is a test text file."
        txt_file_one = SimpleUploadedFile("txt_file_one.txt", txt_content, content_type="text/plain")
        txt_file_two = SimpleUploadedFile("txt_file_two.txt", txt_content, content_type="text/plain")

        data = {
            "base_site": base_site.id,
            "image": txt_file_one,
            "thumbnail": txt_file_two,
            "source": "source",
        }

        response = authorized_client.post(path, data, format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()

        expected_error = {
            "image": ["Upload a valid image. The file you uploaded was either not an image or a corrupted image."],
            "thumbnail": ["Upload a valid image. The file you uploaded was either not an image or a corrupted image."],
        }
        assert response.json() == expected_error

        assert SiteImage.objects.count() == 0

        txt_file_one.close()
        txt_file_two.close()

    def _create_test_image(self) -> SimpleUploadedFile:
        image = Image.new("RGB", (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix=".png")
        image.save(tmp_file)
        tmp_file.seek(0)
        return SimpleUploadedFile("test_image.png", tmp_file.read(), content_type="image/png")
