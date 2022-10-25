from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery.baker import make

from apps.translations.models import Language


class TestStorage:
    def test_always_unique_filename(self):
        original_filename = "my_flag.jpg"
        image = SimpleUploadedFile(original_filename, b"file_content")
        languages = make(Language, flag=image, _quantity=5)
        actual_unique_names = {language.flag.name for language in languages}
        assert len(actual_unique_names) == len(languages)
