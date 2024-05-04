from datetime import datetime
from django.core.management.base import BaseCommand
from django.db.models import Q
from blog.models import Job
import warnings
warnings.simplefilter(action='ignore', category=RuntimeWarning)

class Command(BaseCommand):
    help = 'Remove job listings within a specified date range from a selected database'

    def add_arguments(self, parser):
        parser.add_argument('database', type=str, choices=['first_db', 'second_db', 'third_db', 'all'],
                            help='Database to remove jobs from: first_db, second_db, third_db, or all')
        parser.add_argument('start_date', type=str, help='Start date (MM/DD/YYYY)')
        parser.add_argument('end_date', type=str, help='End date (MM/DD/YYYY)')

    def handle(self, *args, **options):
        database = options['database']
        start_date = datetime.strptime(options['start_date'], '%m/%d/%Y').date()
        end_date = datetime.strptime(options['end_date'], '%m/%d/%Y').date()

        if start_date > end_date:
            self.stdout.write(self.style.ERROR('Start date must be before end date.'))
            return

        db_mapping = {
            'first_db': 'first',
            'second_db': 'second',
            'third_db': 'third'
        }
        databases = [db_mapping[db] for db in db_mapping] if database == 'all' else [db_mapping[database]]

        total_removed = 0
        for db in databases:
            jobs_to_remove = Job.objects.using(db).filter(
                Q(actual_date__gte=start_date) & Q(actual_date__lte=end_date)
            )
            count = jobs_to_remove.count()
            jobs_to_remove.delete()
            total_removed += count
            self.stdout.write(self.style.SUCCESS(f'Removed {count} jobs from {db} from {start_date} to {end_date}.'))

        if database == 'all':
            self.stdout.write(self.style.SUCCESS(f'Total removed {total_removed} jobs from all databases.'))
