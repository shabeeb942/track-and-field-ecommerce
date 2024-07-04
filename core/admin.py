from django.contrib import admin

from .models import Setting


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ("site_name", "site_title")
    list_display_links = ("site_name", "site_title")
    search_fields = ("site_name", "site_title")

    def has_add_permission(self, request):
        if Setting.objects.count() >= 1:
            return False
        return True
