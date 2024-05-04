# Job Posting Database Management System
**[Youtube Video Demo](https://www.youtube.com)**
### DSCI551 | Group48: David Tovmasyan & Jinyang Du & Wenjing Huang
#### The project aims to create a Django-based Database Management System for job postings, which enhance the job search and recruitment process by providing a user-friendly, efficient, and interactive job posting platform.

## Description of directories and what each file does
- [Django Frontend Design](https://github.com/Jinyangd/DSCI551_Group48_Project/tree/main/django_project)
  Our user-Friendly Frontend Django design for the project. 
- [LinkedIn Scrape](https://github.com/Jinyangd/DSCI551_Group48_Project/blob/main/linkedin_scrape.py)
  Code of scraping dataset by using Selenium WebDriver & BeautifulSoup HTML Parser.

## Running
- **Scraping data from LinkedIn**
```shell
python linkedin_scrape.py
```
Download the [example.csv](https://drive.google.com/file/d/1RLI85-oi-JQM9OdJEVLjCz-DFzeScRY5/view?usp=sharing) with pre-processed data, because it took us 2 hours to get the csv file.
- **Getting the Django Webpage**
```shell
python manage.py runserver
```
