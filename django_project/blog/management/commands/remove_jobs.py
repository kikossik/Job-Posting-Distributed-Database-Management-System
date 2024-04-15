from datetime import datetime
from django.core.management.base import BaseCommand
from django.db.models import Q
from blog.models import Job

class Command(BaseCommand):
    # usage: 'python manage.py remove_jobs "MM/DD/YYYY" "MM/DD/YYYY"'
    help = 'Remove job listings within a specified date range'

    def add_arguments(self, parser):
        parser.add_argument('start_date', type=str, help='Start date (MM/DD/YYYY)')
        parser.add_argument('end_date', type=str, help='End date (MM/DD/YYYY)')

    def handle(self, *args, **options):
        start_date = datetime.strptime(options['start_date'], '%m/%d/%Y').date()
        end_date = datetime.strptime(options['end_date'], '%m/%d/%Y').date()

        if start_date > end_date:
            self.stdout.write(self.style.ERROR('Start date must be before end date.'))
            return

        # Directly query the Job model without using a specific database
        jobs_to_remove = Job.objects.filter(
            Q(actual_date__gte=start_date) & Q(actual_date__lte=end_date)
        )

        count = jobs_to_remove.count()
        jobs_to_remove.delete()
        
        self.stdout.write(self.style.SUCCESS(f'Removed {count} jobs from {start_date} to {end_date}.'))
