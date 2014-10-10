"""
    Copyright (c) 2014, Jaime Pajuelo.
    All rights reserved.

    Code released under the BSD 2-Clause license.
"""

from django.template import Library
from urlparse import parse_qs


register = Library()


def update_widget(field, new_attrs):
    old_as_widget = field.as_widget

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        attrs = attrs or {}
        attrs.update(new_attrs)

        return old_as_widget(widget, attrs, only_initial)

    field.as_widget = type(old_as_widget)(as_widget, field, field.__class__)

    return field


@register.filter(name='widget_attrs')
def update_widget_attrs(field, qs):
    new_attrs = dict([(n, v[-1]) for n, v in parse_qs(qs).items()])

    return update_widget(field, new_attrs)


@register.filter(name='class_attr')
def update_class_attr(field, value):
    return update_widget(field, {'class': value})


@register.filter(name='placeholder_attr')
def update_placeholder_attr(field, value):
    return update_widget(field, {'placeholder': value})
