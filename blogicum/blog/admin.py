from django.contrib import admin

from .models import Category, Comment, Location, Post

admin.site.empty_value_display = 'Не задано'


class BaseInline(admin.TabularInline):
    model = Post
    extra = 0


class BaseAdmin(admin.ModelAdmin):
    inlines = (
        BaseInline,
    )


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = (
        'title',
        'slug',
        'is_published',
    )

    list_editable = ('is_published',)
    list_filter = ('title',)
    list_display_links = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'created_at',
        'pub_date',
        'category',
        'location',
        'is_published',
        'title',
        'short_text',
        'image',
    )

    list_editable = (
        'is_published',
        'category',
        'location',
        'pub_date',
        'image',
    )

    list_filter = (
        'category',
        'author',
        'location',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_published=True)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class CommentInline(admin.TabularInline):
    model = Post
    extra = 1


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'created_at',
        'post',
        'text',
        'is_published',
    )

    list_filter = (
        'post',
        'author',
        'created_at',
    )
    list_editable = (
        'is_published',
    )

    list_display_links = (
        'author',
        'post',
    )

    list_display_linkssearch_fields = (
        'text',
        'author',
        'post',
    )

    date_hierarchy = 'created_at'


@admin.register(Location)
class LocationAdmin(BaseAdmin):
    list_display = (
        'name',
        'is_published',
    )

    list_filter = ('name',)
    search_fields = ('name',)
