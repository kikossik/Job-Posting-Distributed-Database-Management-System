# Job Posting Database Management System
### DSCI551 | Group48: David Tovmasyan & Jinyang Du & Wenjing Huang
#### The project aims to create a Django-based Database Management System for job postings, which enhance the job search and recruitment process by providing a user-friendly, efficient, and interactive job posting platform.
**[Implementation Demo](https://www.youtube.com)**

## Description of Directories
- [Django Frontend Design](https://github.com/Jinyangd/DSCI551_Group48_Project/tree/main/django_project)
  Our User-Friendly Frontend Django Design.
- [LinkedIn Scrape](https://github.com/Jinyangd/DSCI551_Group48_Project/blob/main/linkedin_scrape.py)
  Code for scraping dataset by using Selenium WebDriver & BeautifulSoup HTML Parser.

## Running
- **Scraping data from LinkedIn**
```shell
python linkedin_scrape.py
```
Download the [example.csv](https://drive.google.com/file/d/1RLI85-oi-JQM9OdJEVLjCz-DFzeScRY5/view?usp=sharing) with pre-processed data, because it took us 2 hours to get the csv file.
- **Insert the dataset to Webpage**
```shell
python manage.py import_jobs "<location_to_the_csv_file>"
```
- **If you want to delete the job in a time range**
```shell
python manage.py remove_jobs "all" "<start_date>" "<end_date>"
```
- **Get into the Django Webpage**
```shell
python manage.py runserver
```
