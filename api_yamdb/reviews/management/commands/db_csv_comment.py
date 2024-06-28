import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import MyUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            os.path.join(settings.BASE_DIR, 'static', 'data', 'category.csv'),
            'r',
            encoding='utf-8',
        ) as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                Category.objects.create(
                    name=row['name'],
                    slug=row['slug'],
                )

        with open(
            os.path.join(settings.BASE_DIR, 'static', 'data', 'genre.csv'),
            'r',
            encoding='utf-8',
        ) as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                Genre.objects.create(
                    name=row['name'],
                    slug=row['slug'],
                )

        with open(
            os.path.join(settings.BASE_DIR, 'static', 'data', 'titles.csv'),
            'r',
            encoding='utf-8',
        ) as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                Title.objects.create(
                    name=row['name'],
                    year=row['year'],
                    category_id=int(row['category']),
                )

        with open(
            os.path.join(settings.BASE_DIR, 'static', 'data', 'users.csv'),
            'r',
            encoding='utf-8',
        ) as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                MyUser.objects.create(
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=['first_name'],
                    last_name=['last_name'],
                )

        with open(
            os.path.join(settings.BASE_DIR, 'static', 'data', 'review.csv'),
            'r',
            encoding='utf-8',
        ) as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                Review.objects.create(
                    title_id=int(row['title_id']),
                    text=row['text'],
                    author_id=int(row['author']),
                    score=int(row['score']),
                    pub_date=row['pub_date'],
                )

        with open(
            os.path.join(settings.BASE_DIR, 'static', 'data', 'comments.csv'),
            'r',
            encoding='utf-8',
        ) as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                Comment.objects.create(
                    review_id=int(row['review_id']),
                    text=row['text'],
                    author_id=int(row['author']),
                    pub_date=row['review_id'],
                )
