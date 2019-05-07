"""
Django admin page for waffle utils models
"""
from django.contrib import admin

from config_models.admin import KeyedConfigurationModelAdmin


from .forms import WaffleFlagCourseOverrideAdminForm, WaffleFlagDashboardCourseLoadCountAdminForm
from .models import WaffleFlagCourseOverrideModel, WaffleFlagDashboardCourseLoadCount


class WaffleFlagCourseOverrideAdmin(KeyedConfigurationModelAdmin):
    """
    Admin for course override of waffle flags.

    Includes search by course_id and waffle_flag.

    """
    form = WaffleFlagCourseOverrideAdminForm
    search_fields = ['waffle_flag', 'course_id']
    fieldsets = (
        (None, {
            'fields': ('waffle_flag', 'course_id', 'override_choice', 'enabled'),
            'description': 'Enter a valid course id and an existing waffle flag. The waffle flag name is not validated.'
        }),
    )


class WaffleFlagDashboardCourseLoadCountAdmin(admin.ModelAdmin):
    """
    Admin for number of courses to show on dashboard.

    """
    form = WaffleFlagDashboardCourseLoadCountAdminForm
    fieldsets = (
        (None, {
            'fields': ('courses_count', 'enabled'),
            'description': 'Number of courses to show on dashboard.'
        }),
    )

    def has_add_permission(self, request):
        if WaffleFlagDashboardCourseLoadCount.objects.all():
            return False
        else:
            return True


admin.site.register(WaffleFlagCourseOverrideModel, WaffleFlagCourseOverrideAdmin)
admin.site.register(WaffleFlagDashboardCourseLoadCount, WaffleFlagDashboardCourseLoadCountAdmin)
