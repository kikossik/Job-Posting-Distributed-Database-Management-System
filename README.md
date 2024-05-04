# Job Posting Database Management System
### DSCI551 | Group48: David Tovmasyan & Jinyang Du & Wenjing Huang
#### The project aims to create a Django-based Database Management System for job postings, which enhance the job search and recruitment process by providing a user-friendly, efficient, and interactive job posting platform.
**[Youtube Video Demo](https://www.youtube.com)**

## Description of Directories
- [Django Frontend Design](https://github.com/Jinyangd/DSCI551_Group48_Project/tree/main/django_project)
  Our user-Friendly Frontend Django design for the project. 
- [LinkedIn Scrape](https://github.com/Jinyangd/DSCI551_Group48_Project/blob/main/linkedin_scrape.py)
  Code of scraping dataset by using Selenium WebDriver & BeautifulSoup HTML Parser.

## Setup (what language we need to install firstly in the project?)
- **Installation**


## Running
- **Scraping data from LinkedIn**
Download the [example.csv](https://drive.google.com/file/d/1RLI85-oi-JQM9OdJEVLjCz-DFzeScRY5/view?usp=sharing) with pre-processed data, because it took us 2 hours to get the csv file.
Or you can use the code below to try yourself.
```shell
python linkedin_scrape.py
```
- **Getting the Django Webpage**
```shell
python manage.py runserver
```
