from django.contrib import admin
from .models import Task, TestCase, Solution, Group
from .models.group import GroupMembership

admin.site.register(Task)
admin.site.register(TestCase)
admin.site.register(Solution)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'join_code', 'image_tag')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        from django.utils.html import mark_safe
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" />')
        return "No Image"

    image_tag.short_description = 'Image'

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'join_code', 'creator', 'image', 'image_tag')
        }),
    )


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ['group', 'user', 'role', 'joined_at']
    list_filter = ['role']
    search_fields = ['group__name', 'user__username']
