from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'publish', 'author')
    list_filter = ('status', 'author')
    prepopulated_fields = {'slug': ('title',)}
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user_name', 'email', 'comment')
    list_filter = ('post', 'user_name', 'publish')