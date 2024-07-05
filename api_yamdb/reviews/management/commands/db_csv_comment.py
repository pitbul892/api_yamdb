import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import ModifiedUser


class Command(BaseCommand):
    csv_files = {
        'users.csv': ModifiedUser,
        'category.csv': Category,
        'genre.csv': Genre,
        'titles.csv': Title,
        'review.csv': Review,
        'comments.csv': Comment,
    }

    def add_arguments(self, parser):
        parser.add_argument('--user', action='store_true')
        parser.add_argument('--category', action='store_true')
        parser.add_argument('--genre', action='store_true')
        parser.add_argument('--titles', action='store_true')
        parser.add_argument('--review', action='store_true')
        parser.add_argument('--comments', action='store_true')

    def select_optios(self, **options):
        if options['user']:
            self.csv_files = {'users.csv': ModifiedUser}
        if options['category']:
            self.csv_files = {'category.csv': Category}
        if options['genre']:
            self.csv_files = {'genre.csv': Genre}
        if options['titles']:
            self.csv_files = {'titles.csv': Title}
        if options['review']:
            self.csv_files = {'review.csv': Review}
        if options['comments']:
            self.csv_files = {'comments.csv': Comment}
        return self.csv_files

    def handle(self, *args, **options):
        csv_files = self.select_optios(**options)

        for csv_file, model in csv_files.items():
            try:
                f = open(
                    os.path.join(settings.BASE_DIR, 'static/data/', csv_file),
                    encoding='utf-8',
                )
            except OSError:
                self.stdout.write(f'The file {csv_file} could not be opened')
                continue
            with f:
                reader = csv.DictReader(f)
                try:
                    model.objects.bulk_create(model(**row) for row in reader)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'{model.__name__} imported from {csv_file}'
                        )
                    )
                except Exception as error:
                    self.stdout.write(
                        self.style.ERROR(
                            f'{model.__name__} error {error} imported'
                        )
                    )
