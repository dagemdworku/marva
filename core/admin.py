from django.contrib import admin

from django.contrib import admin
from .models import Post, Comment, ChatConversation


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "views_count", "shared_count")
    search_fields = ("content",)
    ordering = ("-created_at",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "creator_id", "created_at", "post", "parent_comment")
    search_fields = ("comment",)
    ordering = ("-created_at",)


@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "chat_timestamp", "user_type")
    search_fields = ("content",)
    ordering = ("-chat_timestamp",)
