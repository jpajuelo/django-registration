"""
    Copyright (c) 2014, Jaime Pajuelo.
    All rights reserved.

    Code released under the BSD 2-Clause license.
"""

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import datetime
from registration import app_settings, app_templates
from registration.utils import hash_sequence, is_sha1_hashed


class ActivationCodeManager(models.Manager):

    def activate_inactive_user(self, code):
        if not is_sha1_hashed(code):
            return (False, None)

        try:
            instance = self.get(code=code)
        except self.model.DoesNotExist:
            return (False, None)

        if instance.is_expired():
            return (False, instance)

        user = instance.user
        credentials = {
            'username': user.username,
            'password': user.password
        }

        user.is_active = True
        user.set_password(credentials['password'])
        user.save()

        instance.delete()

        return (True, {'user': user, 'credentials': credentials})

    def create_inactive_user(self, user):
        user.is_active = False
        user.save()

        return self.create(user=user, code=hash_sequence(user.username))


class ActivationCode(models.Model):

    user = models.ForeignKey(User, unique=True)
    code = models.CharField(max_length=40)

    objects = ActivationCodeManager()

    def __unicode__(self):
        return "for user '%s'" % self.user.username

    def get_absolute_url(self, viewname='activate_user'):
        return reverse(viewname, args=[self.code])

    def get_expiration_date(self):
        return self.user.date_joined + datetime.timedelta(days=app_settings.CONFIRMATION_DAYS)
    get_expiration_date.short_description = "Expiration date"

    def is_expired(self):
        return self.get_expiration_date() <= timezone.now()
    is_expired.short_description = "Expired"

    def send_confirmation_email(self, site):
        context = {
            'activation_url': self.get_absolute_url(),
            'confirmation_days': app_settings.CONFIRMATION_DAYS,
            'site': site,
            'user': self.user,
        }

        subject = app_templates.render_to_string('CONF_MSG_SUBJ', context, False)
        message = app_templates.render_to_string('CONF_MSG_BODY', context)

        self.user.email_user(subject, message)
