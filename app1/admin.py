from django.contrib import admin

from .models import SoftwareRelease, Component


# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Component
    extra = 2


class SoftwareReleaseAdmin(admin.ModelAdmin):
    # fields = ['pub_date', 'product_name']

    fieldsets = [
        (None, {'fields': ['product_name']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

    list_display = ('product_name', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']

    search_fields = ['product_name']


class ComponentAdmin(admin.ModelAdmin):
    fields = ['component_name', 'version']

    list_display = ('component_name', 'version')

    search_fields = ['component_name']


admin.site.register(SoftwareRelease, SoftwareReleaseAdmin)
admin.site.register(Component, ComponentAdmin)
