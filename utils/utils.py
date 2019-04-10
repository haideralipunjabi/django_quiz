from django.core.exceptions import ValidationError

from django_quiz import settings


def validate_only_one_instance(obj):
    """ Ensures that the model can have only one instance """
    # Thanks to http://stackoverflow.com/a/6436008/4591121
    model = obj.__class__
    if model.objects.count() > 0 and obj.id != model.objects.get().id:
        raise ValidationError(
            "You can create only one %s instance, edit the previous one to make any changes." % model.__name__)


def get_default_background():
    return settings.STATIC_URL + "default_background.png"
