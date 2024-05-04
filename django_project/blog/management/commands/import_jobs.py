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
        jobs_by_db = {'first': [], 'second': [], 'third': []}
        count = 0

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'posted time' in row:
                    row['date'] = Job.parse_relative_date(row['posted time'])
                job = Job.create_from_csv_row(row)
                
                if job:
                    db_name = self.get_db_for_job(job.job_title)  # Use job title for hashing
                    if db_name:
                        jobs_by_db[db_name].append(job)
                    else:
                        count += 1
                        print(f"Skipping job due to unknown title hash.")
                else:
                    count += 1
        print(f"Skipped {count} invalid rows.")

        for db_name, jobs in jobs_by_db.items():
            Job.objects.using(db_name).bulk_create(jobs, batch_size=100)
            self.stdout.write(self.style.SUCCESS(f'Bulk imported {len(jobs)} jobs into {db_name} from {csv_file_path}'))

    def hash_by_title_length(self, title):
        # Initialize the hash value
        hashVal = 0
        # Accumulate the ASCII values of each character in the title
        for char in title:
            hashVal += ord(char)
        # Mod by 3 since we have 3 databases
        return hashVal % 3

    def get_db_for_job(self, job_title):
        index = self.hash_by_title_length(job_title)
        if index == 0:
            return 'first'
        elif index == 1:
            return 'second'
        elif index == 2:
            return 'third'
        return None

