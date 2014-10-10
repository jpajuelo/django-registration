"""
    Copyright (c) 2014, Jaime Pajuelo.
    All rights reserved.

    Code released under the BSD 2-Clause license.
"""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.sites.models import get_current_site
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic.edit import FormView

import hashlib
import json
import re
import uuid


SHA1_RE = re.compile(r'^[a-f0-9]+$')


def hash_sequence(sequence):
    salt = uuid.uuid4().hex

    return hashlib.sha1(salt.encode() + sequence.encode()).hexdigest()


def is_sha1_hashed(sequence):
    return SHA1_RE.search(sequence) and len(sequence) == 40


class LoginRedirectMixin(object):

    url = None

    def get_context_data(self, **kwargs):
        if 'site' not in kwargs:
            kwargs['site'] = get_current_site(self.request)

        return kwargs

    def get_redirect_url(self):
        if self.url is None:
            return settings.LOGIN_REDIRECT_URL

        return self.url

    def redirect(self, credentials, message=None):
        login(self.request, authenticate(**credentials))

        if message is not None:
            messages.success(self.request, message)

        return redirect(self.get_redirect_url())


class AjaxFormView(FormView):

    query_name = 'field'

    def get_field_name(self, request):
        return request.GET[self.query_name]

    def is_ajax_allowed(self, request):
        return request.is_ajax() and self.query_name in request.GET

    def post(self, request, *args, **kwargs):
        if self.is_ajax_allowed(request):
            return self.validate_field(request)

        return FormView.post(self, request, *args, **kwargs)

    def validate_field(self, request):
        field_name = self.get_field_name(request)
        form = self.get_form(self.get_form_class())

        content = json.dumps({
            'is_valid': field_name not in form.errors,
            'errors': form.errors.get(field_name, [])
        })

        return HttpResponse(content, content_type='application/json')
