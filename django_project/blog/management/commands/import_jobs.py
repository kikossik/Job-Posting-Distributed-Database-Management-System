import warnings
from django.core.management.base import BaseCommand
import csv
from blog.models import Job
warnings.simplefilter(action='ignore', category=RuntimeWarning)

class Command(BaseCommand):
    help = 'Imports job listings from a specified CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='The path to the CSV file to import')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path']
        jobs_by_db = {'east_coast_db': [], 'west_coast_db': [], 'mid_states_db': []}
        count = 0

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'posted time' in row:
                    row['date'] = Job.parse_relative_date(row['posted time'])
                job = Job.create_from_csv_row(row)
                if job:
                    # Determine the appropriate database
                    db_name = self.get_db_for_job(job.state_code)
                    if db_name:
                        jobs_by_db[db_name].append(job)
                    else:
                        count += 1
                        print(f"Skipping job due to unknown state code: {job.state_code}")
                else:
                    count += 1
                    print("Skipping invalid row...")
        print(f"Skipped {count} invalid rows.")

        # Use bulk_create for each database separately
        for db_name, jobs in jobs_by_db.items():
            Job.objects.using(db_name).bulk_create(jobs, batch_size=100)
            self.stdout.write(self.style.SUCCESS(f'Bulk imported {len(jobs)} jobs into {db_name} from {csv_file_path}'))

    def get_db_for_job(self, state_code):
        EAST_COAST_STATES = {'CT', 'DE', 'FL', 'GA', 'ME', 'MD', 'MA', 'NH', 'NJ', 'NY', 'NC', 'PA', 'RI', 'SC', 'VA', 'VT', 'WV'}
        WEST_COAST_STATES = {'CA', 'OR', 'WA', 'AK', 'HI'}
        MID_STATES = {'AL', 'AZ', 'AR', 'CO', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'MN', 'MS', 'MO', 'MT', 'MI', 'NE', 'NV', 'NM', 'ND', 'OH', 'OK', 'SD', 'TN', 'TX', 'UT', 'WI', 'WY'}
        if state_code in EAST_COAST_STATES:
            return 'east_coast_db'
        elif state_code in WEST_COAST_STATES:
            return 'west_coast_db'
        elif state_code in MID_STATES:
            return 'mid_states_db'
        return None
