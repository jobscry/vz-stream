from django.contrib import admin
from models import Source, Entry


def make_enabled(SourceAdmin, request, queryset):
    queryset.update(enabled=True)
make_enabled.short_description = 'Enable selected sources'

def make_disabled(SourceAdmin, request, queryset):
    queryset.update(enabled=False)
make_disabled.short_description = 'Disable selected sources'

def reset_source(SourceAdmin, request, queryset):
    queryset.update(etag=None, last_modified=None)
reset_source.short_description = 'Reset selected sources'

class SourceAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_modified'
    fieldsets = (
        (None, {
            'fields': ('name', 'url', 'enabled')
        }),
        ('Feed Options', {
            'fields': ('feed_type', 'auto_link')
        }),
        ('Info', {
            'fields': ('last_update_successful', 'etag', 'last_modified', 'last_status_code', 'error_message')
        })
    )
    list_display = ('name', 'num_entries', 'feed_type', 'enabled', 'last_status_code',
        'last_modified', 'created_on', 'modified')
    actions = [make_enabled, make_disabled, reset_source]

    def num_entries(self, obj):
        return Entry.objects.filter(source=obj.pk).count()

admin.site.register(Source, SourceAdmin)

class EntryAdmin(admin.ModelAdmin):
    list_display = ('source', 'created_on', 'retrieved_on')
    list_filter = ('source', )

admin.site.register(Entry, EntryAdmin)