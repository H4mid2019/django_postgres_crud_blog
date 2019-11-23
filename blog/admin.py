from django.contrib import admin
from .models import Post, Category, Media


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
