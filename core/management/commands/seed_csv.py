import csv
import os
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from core.models import Post, Comment


class Command(BaseCommand):
    help = 'Seed the database with posts and comments from CSV files.'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
        seed_data_dir = os.path.join(base_dir, 'seed_data')

        # Seed Posts
        posts_file = os.path.join(seed_data_dir, 'posts.csv')
        if os.path.exists(posts_file):
            with open(posts_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                count = 0
                for row in reader:
                    post_id = int(row['id'])
                    if not Post.objects.filter(id=post_id).exists():
                        count += 1
                        Post.objects.create(
                            id=post_id,
                            content=row['content'],
                            created_at=parse_datetime(row['created_at']),
                            views_count=int(row['views_count']),
                            shared_count=int(row['shared_count'])
                        )
            self.stdout.write(self.style.SUCCESS(
                f'[{count}] Posts seeded successfully.'))
        else:
            self.stdout.write(self.style.WARNING('posts.csv not found.'))

        # Seed Comments
        comments_file = os.path.join(seed_data_dir, 'comments.csv')
        if os.path.exists(comments_file):
            with open(comments_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                count = 0
                for row in reader:
                    comment_id = int(row['id'])
                    if not Comment.objects.filter(id=comment_id).exists():
                        count += 1
                        post = Post.objects.get(id=int(row['post_id']))
                        parent_comment = Comment.objects.filter(
                            id=row['parent_comment_id']).first() if row['parent_comment_id'] else None
                        Comment.objects.create(
                            id=comment_id,
                            comment=row['comment'],
                            creator_id=row['creator_id'],
                            created_at=parse_datetime(row['created_at']),
                            post=post,
                            parent_comment=parent_comment
                        )
            self.stdout.write(self.style.SUCCESS(
                f'[{count}] Comments seeded successfully.'))
        else:
            self.stdout.write(self.style.WARNING('comments.csv not found.'))
