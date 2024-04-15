from django.core.management.base import BaseCommand
import csv
# from blog.management.commands.date_manipulation import parse_relative_date
from blog.models import Job  

class Command(BaseCommand):
    # usage: 'python manage.py import_jobs path/to/csv_file.csv'
    #         python manage.py import_jobs "C:\\Users\\mobis\\Downloads\\final_job_postings.csv"
    help = 'Imports job listings from a specified CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='The path to the CSV file to import')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path']
        jobs_to_create = []
        count = 0

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:                
                row['date'] = Job.parse_relative_date(row['posted time'])
                job = Job.create_from_csv_row(row)
                if job is not None:
                    jobs_to_create.append(job)
                else:
                    count += 1
                    print("Skipping invalid row...")
        print(f"Skipped {count} invalid rows.")
                    

        # Use bulk_create to add all new Job instances to the database
        Job.objects.bulk_create(jobs_to_create, batch_size=100)
        self.stdout.write(self.style.SUCCESS(f'Bulk imported {len(jobs_to_create)} jobs from {csv_file_path}'))