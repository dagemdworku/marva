from django.test import TestCase
from core.models import Post, Comment, ChatConversation


class TestPostModel(TestCase):
    def test_create_post(self):
        post = Post.objects.create(content="Sample post")
        self.assertEqual(post.content, "Sample post")
        self.assertEqual(post.views_count, 0)
        self.assertEqual(post.shared_count, 0)


class TestCommentModel(TestCase):
    def test_create_comment(self):
        post = Post.objects.create(content="Test Post")
        comment = Comment.objects.create(
            comment="This is a comment",
            creator_id="user1",
            post=post,
        )
        self.assertEqual(comment.comment, "This is a comment")
        self.assertEqual(comment.post, post)


class TestChatConversationModel(TestCase):
    def test_create_chat(self):
        chat = ChatConversation.objects.create(
            content="Hello from user",
            user_type="user",
        )
        self.assertEqual(chat.content, "Hello from user")
        self.assertEqual(chat.user_type, "user")
