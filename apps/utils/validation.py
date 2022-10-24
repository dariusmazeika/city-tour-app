from django.core.exceptions import ValidationError
from django.template import Template, exceptions


def check_template(template):
    """Checks whether the template is valid"""
    try:
        Template(template)
    except exceptions.TemplateSyntaxError:
        raise ValidationError("Invalid template syntax")
