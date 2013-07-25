# -*- coding: utf-8 -*-
from __builtin__ import object

__author__ = 'bteam'

from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.contrib.admin.models import LogEntry, DELETION, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType


def construct_change_message(form, formsets):
    """
    Construct a change message from a changed object.
    """
    change_message = []
    if form.changed_data:
        fields_changed = u'Изменено '
        for f in form.changed_data:
            fields_changed += u'%s, ' % form[f].label
        change_message.append(fields_changed[:-1])

    if formsets:
        for formset in formsets:
            for added_object in formset.new_objects:
                change_message.append(_('Added %(name)s "%(object)s".')
                                      % {'name': force_unicode(added_object._meta.verbose_name),
                                         'object': force_unicode(added_object)})
            for changed_object, changed_fields in formset.changed_objects:
                fields_changed = ''
                for f in changed_fields:
                    fields_changed += '%s, ' % formset.empty_form[f].label
                change_message.append(_('Changed %(list)s for %(name)s "%(object)s".')
                                      % {'list': fields_changed[:-1],
                                         'name': force_unicode(changed_object._meta.verbose_name),
                                         'object': force_unicode(changed_object)})
            for deleted_object in formset.deleted_objects:
                change_message.append(_('Deleted %(name)s "%(object)s".')
                                      % {'name': force_unicode(deleted_object._meta.verbose_name),
                                         'object': force_unicode(deleted_object)})
    change_message = ' '.join(change_message)
    return change_message or _('No fields changed.')


def log_addition(request, object):
    """
    Log that an object has been successfully added.

    The default implementation creates an admin LogEntry object.
    """

    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_unicode(object),
        action_flag=ADDITION
    )


def log_change(request, object, message):
    """
    Log that an object has been successfully changed.

    The default implementation creates an admin LogEntry object.
    """

    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_unicode(object),
        action_flag=CHANGE,
        change_message=message
    )


def log_deletion(request, object, object_repr):
    """
    Log that an object will be deleted. Note that this method is called
    before the deletion.

    The default implementation creates an admin LogEntry object.
    """

    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=object_repr,
        action_flag=DELETION
    )
  
