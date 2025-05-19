from django.db import models
from django.utils import timezone


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    views_count = models.PositiveIntegerField(default=0)
    shared_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Post {self.id}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.TextField()
    creator_id = models.CharField(max_length=255)  # could be user or agent
    created_at = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")

    def __str__(self):
        return f"Comment {self.id} on Post {self.post.id}"


class ChatConversation(models.Model):
    USER_CHOICES = [
        ("user", "User"),
        ("llm", "LLM"),  # Raw LLM access, fallback mode
        ("strategist", "Marketing Strategist"),
        ("material_creator", "Material Creator"),
        ("analyzer", "Social Media Analyzer"),
        ("post_replier", "Post Replier"),
    ]

    id = models.AutoField(primary_key=True)
    chat_timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    user_type = models.CharField(max_length=16, choices=USER_CHOICES)

    def __str__(self):
        return f"Chat ({self.user_type}) at {self.chat_timestamp}"
