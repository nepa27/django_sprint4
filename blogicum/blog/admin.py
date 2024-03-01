from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.utils.safestring import mark_safe

from .models import Post, Category, Comment, Location


@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'category',
        'pub_date',
        'author',
        'is_published',
        'get_image',

    )
    readonly_fields = ('get_image',)
    list_display_links = (
        'title',
        'category'
    )
    list_filter = (
        'category',
        'author',
        'is_published'
    )
    list_editable = (
        'text',
        'pub_date',
        'author',
        'is_published'
    )
    search_fields = (
        'title',
    )

    def get_image(self, obj):
        if not (obj.pk and obj.image):
            return ''
        return mark_safe(f'<img src={obj.image.url} width="80" height="60">')
    get_image.short_description = 'Изображение'

    PAGINATION = 10


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
    )
    list_filter = (
        'created_at',
        'is_published')
    search_fields = (
        'name',
    )


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at'
    )
    list_editable = (
        'description',
        'is_published',
        'slug'
    )
    list_filter = (
        'is_published',
    )
    search_fields = (
        'title',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
    )


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'posts_count',
    )

    @admin.display(description='Кол-во постов у пользователя')
    def posts_count(self, obj):
        return obj.posts.count()
