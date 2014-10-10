"""
    Copyright (c) 2014, Jaime Pajuelo.
    All rights reserved.

    Code released under the BSD 2-Clause license.
"""

from django.conf import settings
from django.template.base import TemplateDoesNotExist
from django.template.loader import render_to_string


__version__ = (0, 0, 1)


def get_version():
    return ".".join(str(d) for d in __version__)


class SettingManager(object):

    default_settings = {
        'CONFIRMATION_DAYS': 7,
        'CONFIRMATION_REQUIRED': False,
        'FIELD_VALIDATION_ALLOWED': False
    }

    def __init__(self, user_settings=None):
        self.user_settings = user_settings or {}

    def __getattr__(self, attr):
        if attr not in self.default_settings:
            args = (self.__class__.__name__, attr)
            raise AttributeError("'%s' object has no attribute '%s'" % args)

        if attr in self.user_settings:
            return self.user_settings[attr]

        return self.default_settings[attr]

app_settings = SettingManager(getattr(settings, 'REGISTRATION', None))


class TemplateManager(object):

    txt_templates = {
        'CONF_MSG_BODY': "confirmation_message_body",
        'CONF_MSG_SUBJ': "confirmation_message_subject",
        'REG_SUCCESS_MSG': "registration_success_message"
    }

    def __init__(self, template_dir):
        self.template_dir = template_dir

        if not self.template_dir.endswith('/'):
            self.template_dir += '/'

    def __getattr__(self, name):
        if name not in self.txt_templates:
            args = (self.__class__.__name__, name)
            raise AttributeError("'%s' object has no attribute '%s'" % args)

        return self.template_dir + self.txt_templates[name] + ".txt"

    def render_to_string(self, name, context=None, newlines=True):
        template_name = getattr(self, name)
        context = context or {}

        try:
            rendered = render_to_string(template_name, context)
        except TemplateDoesNotExist:
            return "'%s' template does not exist" % template_name

        return rendered if newlines else "".join(rendered.splitlines())

app_templates = TemplateManager("registration")
