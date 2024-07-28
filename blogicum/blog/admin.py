from .models import Category, Post, Location
from django.contrib import admin

admin.site.empty_value_display = 'Не задано'


class BaseInline(admin.TabularInline):
    model = Post
    extra = 0


class BaseAdmin(admin.ModelAdmin):
    inlines = (
        BaseInline,
    )


class CategoryAdmin(BaseAdmin):
    list_display = (
        'title',
        'is_published',
    )

    list_editable = (
        'is_published',
    )


class LocationAdmin(BaseAdmin):
    list_display = (
        'name',
        'is_published',
    )

    list_editable = (
        'is_published',
    )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'created_at',
        'pub_date',
        'category',
        'location',
        'is_published',
        'title',
        'short_text'
    )

    list_editable = (
        'is_published',
        'category',
        'location',
        'pub_date',
    )

    list_filter = (
        'category',
        'author',
        'location',
    )

    list_display_links = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
