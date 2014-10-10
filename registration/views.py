"""
    Copyright (c) 2014, Jaime Pajuelo.
    All rights reserved.

    Code released under the BSD 2-Clause license.
"""

from django.http.response import Http404
from django.views.generic.base import TemplateView

from registration import app_settings, app_templates
from registration.forms import RegistrationForm
from registration.models import ActivationCode
from registration.utils import AjaxFormView, LoginRedirectMixin


class UserRegistrationView(LoginRedirectMixin, AjaxFormView):

    confirmation_required = None
    form_class = RegistrationForm
    http_method_names = ['get', 'post']
    template_name = 'registration/registration_form.html'

    def get_confirmation_required(self):
        if self.confirmation_required is None:
            return app_settings.CONFIRMATION_REQUIRED

        return self.confirmation_required

    def is_ajax_allowed(self, request):
        if not app_settings.FIELD_VALIDATION_ALLOWED:
            return False

        return AjaxFormView.is_ajax_allowed(self, request)

    def form_valid(self, form):
        if self.get_confirmation_required():
            return self.send_confirmation(form)

        return self.complete_registration(form)

    def complete_registration(self, form):
        user = form.save(commit=True)
        credentials = form.get_credentials()

        context = self.get_context_data(user=user)
        message = app_templates.render_to_string('REG_SUCCESS_MSG', context)

        return self.redirect(credentials, message)

    def send_confirmation(self, form):
        user = form.save(commit=False)
        activation_code = ActivationCode.objects.create_inactive_user(user)

        context = self.get_context_data(registration_done=True, user=user)

        activation_code.send_confirmation_email(context['site'])

        return self.render_to_response(context)

register_user = UserRegistrationView.as_view


class UserActivationView(LoginRedirectMixin, TemplateView):

    http_method_names = ['get']

    def get(self, request, code):
        valid, instance = ActivationCode.objects.activate_inactive_user(code)

        if not valid:
            raise Http404

        context = self.get_context_data(user=instance['user'])
        message = app_templates.render_to_string('REG_SUCCESS_MSG', context)

        return self.redirect(instance['credentials'], message)

activate_user = UserActivationView.as_view
