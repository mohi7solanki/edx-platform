"""
Models for configuring waffle utils.
"""
from django.db import models
from django.db.models import CharField, IntegerField, BooleanField
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from opaque_keys.edx.django.models import CourseKeyField
from six import text_type

from config_models.models import ConfigurationModel
from openedx.core.lib.cache_utils import request_cached


class WaffleFlagCourseOverrideModel(ConfigurationModel):
    """
    Used to force a waffle flag on or off for a course.

    .. no_pii:
    """
    OVERRIDE_CHOICES = Choices(('on', _('Force On')), ('off', _('Force Off')))
    ALL_CHOICES = OVERRIDE_CHOICES + Choices('unset')

    KEY_FIELDS = ('waffle_flag', 'course_id')

    # The course that these features are attached to.
    waffle_flag = CharField(max_length=255, db_index=True)
    course_id = CourseKeyField(max_length=255, db_index=True)
    override_choice = CharField(choices=OVERRIDE_CHOICES, default=OVERRIDE_CHOICES.on, max_length=3)

    @classmethod
    @request_cached()
    def override_value(cls, waffle_flag, course_id):
        """
        Returns whether the waffle flag was overridden (on or off) for the
        course, or is unset.

        Arguments:
            waffle_flag (String): The name of the flag.
            course_id (CourseKey): The course id for which the flag may have
                been overridden.

        If the current config is not set or disabled for this waffle flag and
            course id, returns ALL_CHOICES.unset.
        Otherwise, returns ALL_CHOICES.on or ALL_CHOICES.off as configured for
            the override_choice.

        """
        if not course_id or not waffle_flag:
            return cls.ALL_CHOICES.unset

        effective = cls.objects.filter(waffle_flag=waffle_flag, course_id=course_id).order_by('-change_date').first()
        if effective and effective.enabled:
            return effective.override_choice
        return cls.ALL_CHOICES.unset

    class Meta(object):
        app_label = "waffle_utils"
        verbose_name = 'Waffle flag course override'
        verbose_name_plural = 'Waffle flag course overrides'

    def __unicode__(self):
        enabled_label = "Enabled" if self.enabled else "Not Enabled"
        return u"Course '{}': Persistent Grades {}".format(text_type(self.course_id), enabled_label)


class WaffleFlagDashboardCourseLoadCount(models.Model):
    """
    Flag for number of courses to show on dashboard.

    """
    # The course count that will be shown on dashboard.
    courses_count = IntegerField(default=250)
    enabled = BooleanField(default=True)

    class Meta(object):
        app_label = "waffle_utils"
        verbose_name = 'Waffle flag Lms Dashboard Course Count'
        verbose_name_plural = 'Waffle flag Lms Dashboard Course Count'

    def __unicode__(self):
        if self.enabled:
            count = self.courses_count
        else:
            count = 250
        return u"Dashboard is set to show {} Courses".format(count)
