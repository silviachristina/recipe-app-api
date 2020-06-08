# default python package that makes our aplication sleep for few seconds
import time
# use to test if data base connect will available
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""
    # as a args you can pass something like the amout of seconds of the timeout
    def handle(self, *args, **options):
        # print some in the screen in a maagement command
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available'))
