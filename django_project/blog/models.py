from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import re
from datetime import datetime, timedelta

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

class Job(models.Model):
    job_title = models.CharField(max_length=100)
    # requirements = models.TextField(max_length=200)
    # date_posted = models.DateTimeField(default=timezone.now)
    agency = models.CharField(max_length=255, default="")
    location = models.CharField(max_length=100, default="")
    link = models.TextField(default="")
    description = models.TextField(default="")
    salary = models.CharField(max_length=50, default="")
    date_posted = models.CharField(max_length=20, default=timezone.now)
    seniority_level = models.CharField(max_length=50, default="")
    employment_type = models.CharField(max_length=50, default="")
    job_function = models.CharField(max_length=255, default="")
    industries = models.CharField(max_length=255, default="")
    state_code = models.CharField(max_length=2, blank=True, default="")  # New field for partitioning
    actual_date = models.DateTimeField(default=timezone.now)

    @classmethod
    def create_from_csv_row(cls, row):
        # Logic to extract state code from location
        state_code = row['location'].split(',')[-1].strip()[-2:]
        if state_code in states:
            formatted_date = cls.parse_relative_date(row['posted time']) # assuming you want a date object
            
            # formatted_date = datetime.strftime(formatted_date, '%B/%d/%Y')
            # formatted_date = formatted_date.strftime('%B %d, %Y')
            return cls(
                job_title=row['title'],
                agency=row['company'],
                location=row['location'],
                link=row['link'],
                description=row['description'],
                salary=row['salary'],
                date_posted=row['posted time'],
                seniority_level=row['seniority_level'],
                employment_type=row['employment_type'],
                job_function=row['job_function'],
                industries=row['industries'],
                state_code=state_code,
                actual_date = formatted_date
            )
        return None
    
    @classmethod
    def parse_relative_date(cls, text):
        current_time = datetime.now()
        numbers = re.findall(r'\d+', text)
        if not numbers:
            return current_time  # Default to current time if no number found

        number = int(numbers[0])  # The first number should be the quantity of time units
        if 'day' in text:
            return current_time - timedelta(days=number)
        elif 'month' in text:
            return current_time - timedelta(days=number * 30)  # Approximation of a month
        elif 'year' in text:
            return current_time - timedelta(days=number * 365)  # Approximation of a year
        else:
            return current_time  # Default to current time if no time unit found
        
    def formatted_actual_date(self):
        return self.actual_date.strftime('%B %d, %Y')
    
    def __str__(self):
        return self.job_title

    def get_absolute_url(self):
        return reverse('job-detail', kwargs={'pk': self.pk})


# from django.db import models
# from django.utils import timezone
# from django.contrib.auth.models import User
# from django.urls import reverse
#
# # Import the hash function
# from .hash_function import hash_function
#
#
# class Job(models.Model):
#     job_title = models.CharField(max_length=100)
#     requirements = models.TextField(max_length=200)
#     date_posted = models.DateTimeField(default=timezone.now)
#     company = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.job_title
#
#     def get_absolute_url(self):
#         return reverse('job-detail', kwargs={'pk': self.pk})
#
#     def save(self, *args, **kwargs):
#         # Calculate the hash value based on the job title
#         hash_value = hash_function(self)
#
#         # Assign the appropriate database alias based on the hash value
#         if hash_value == 0:
#             self._state.db = 'db_0'  # Assign the alias for database 1
#         elif hash_value == 1:
#             self._state.db = 'db_1'  # Assign the alias for database 2
#         else:
#             self._state.db = 'db_2'  # Assign the alias for database 3
#
#         # Call the original save method
#         super().save(*args, **kwargs)
