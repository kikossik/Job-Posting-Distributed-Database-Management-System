#!/usr/bin/env python
# coding: utf-8

# Import necessary packages for web scraping and logging
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

# Configure logging settings
logging.basicConfig(filename="scraping.log", level=logging.INFO)

# Main code implemented from this person on GitHub: https://github.com/hossam-elshabory/LinkedIn-Job-Selenium-Scrapper
# Adjustments have been made to pull additional data from the listings
def scrape_linkedin_jobs(job_title: str, location: str, pages: int = None) -> list:
    """
    Scrape job listings from LinkedIn based on job title and location.

    Parameters
    ----------
    job_title : str
        The job title to search for on LinkedIn.
    location : str
        The location to search for jobs in on LinkedIn.
    pages : int, optional
        The number of pages of job listings to scrape. If None, all available pages will be scraped.

    Returns
    -------
    list of dict
        A list of dictionaries, where each dictionary represents a job listing
        with the following keys: 'job_title', 'company_name', 'location', 'posted_date',
        and 'job_description'.
    """

    # Log a message indicating that we're starting a LinkedIn job search
    logging.info(f'Starting LinkedIn job scrape for "{job_title}" in "{location}"...')

    # Sets the pages to scrape if not provided
    pages = pages or 1

    # Set up Chrome options to maximize the window
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Set up the Selenium web driver with the Chrome options
    driver = webdriver.Chrome(options=options)

    # Navigate to the LinkedIn job search page with the given job title and location
    driver.get(
        f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}"
    )

    # Scroll through the first 50 pages of search results on LinkedIn
    for i in range(pages):

        # Log the current page number
        logging.info(f"Scrolling to bottom of page {i+1}...")

        # Scroll to the bottom of the page using JavaScript
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            # Wait for the "Show more" button to be present on the page
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div/main/section[2]/button")
                )
            )
            # Click on the "Show more" button
            element.click()

        # Handle any exception that may occur when locating or clicking on the button
        except Exception:
            # Log a message indicating that the button was not found and we're retrying
            logging.info("Show more button not found, retrying...")

        # Wait for a random amount of time before scrolling to the next page
        time.sleep(random.choice(list(range(3, 7))))

    # Scrape the job postings
    jobs = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_listings = soup.find_all(
        "div",
        class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card",
    )

    try:
        for job in job_listings:
            # Extract job details

            # job title
            job_title = job.find("h3", class_="base-search-card__title").text.strip()
            # job company
            job_company = job.find(
                "h4", class_="base-search-card__subtitle"
            ).text.strip()
            # job location
            job_location = job.find(
                "span", class_="job-search-card__location"
            ).text.strip()

            # job link
            apply_link = job.find("a", class_="base-card__full-link")["href"]

            # Navigate to the job posting page and scrape the description
            driver.get(apply_link)

            # Sleeping randomly
            time.sleep(random.choice(list(range(5, 11))))

            
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Modified parameters
            # Added additional_info to find additional job details
            additional_info = soup.find_all('span', attrs={'class': 'description__job-criteria-text description__job-criteria-text--criteria'})
            # Used find_job_attribute function to find job description and other attributes
            job_description = find_job_attribute(soup, "div", "description__text description__text--rich", False)
            salary = find_job_attribute(soup, "div", "compensation__salary-range", False)
            posted_time = find_job_attribute(soup, "span", "posted-time-ago__text topcard__flavor--metadata", False)
            additional_info_table = find_job_attribute(additional_info, None, None, True)

            # Add job details to the jobs list
            jobs.append(
                {
                    "title": job_title,
                    "company": job_company,
                    "location": job_location,
                    "link": apply_link,
                    "description": job_description,
                    "salary": salary,
                    "posted time": posted_time,
                    "seniority_level": additional_info_table[0],
                    "employment_type": additional_info_table[1],
                    "job_function": additional_info_table[2],
                    "industries": additional_info_table[3]
                }
            )
            # Logging scrapped job with company and location information
            logging.info(f'Scraped "{job_title}" at {job_company} in {job_location}...')

    # Catching any exception that occurs in the scrapping process
    except Exception as e:
        # Log an error message with the exception details
        logging.error(f"An error occurred while scraping jobs: {str(e)}")

        # Return the jobs list that has been collected so far
        # This ensures that even if the scraping process is interrupted due to an error, we still have some data
        return jobs

    # Close the Selenium web driver
    driver.quit()

    # Return the jobs list
    return jobs


# Created a function to find job attributes
def find_job_attribute(soup, type, name, table):
    """
    Find and extract the job description from a webpage using BeautifulSoup.

    Parameters:
    - driver: The web driver object used to navigate the webpage.
    - type: The type of HTML element to search for (e.g., 'div', 'span', etc.).
    - name: The class name or attribute value of the HTML element to search for.
    - table: Boolean variable indicating whether the job details are in a table format.

    Returns:
    - attribute: The extracted job description text, or None if not found.
    """
    if table == True:
        seniority_level = soup[0].text.strip()
        employment_type = soup[1].text.strip()
        job_function = soup[2].text.strip()
        industries = soup[3].text.strip()
        return [seniority_level, employment_type, job_function, industries]
    else:
        try:
            # Find the job description element and extract its text
            attribute = soup.find(
                type, class_=name
            ).text.strip()
        except AttributeError:
            attribute = None
            logging.warning(
                "AttributeError occurred while retrieving job description."
            )
    return attribute


def save_job_data(data: dict) -> None:
    """
    Save job data to a CSV file.

    Args:
        data: A dictionary containing job data.

    Returns:
        None
    """

    # Create a pandas DataFrame from the job data dictionary
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file without including the index column
    df.to_csv("jobs.csv", index=False)

    # Log a message indicating how many jobs were successfully scraped and saved to the CSV file
    logging.info(f"Successfully scraped {len(data)} jobs and saved to jobs.csv")


# Getting job listings for 18 fastest growing jobs between 2022-2032 (from Bureau of Labor Statistics)
job_list = ["Wind turbine service technicians","Nurse practitioners",
            "Data scientists","Statisticians","Information security analysts",
            "Medical and health services managers","Epidemiologists",
            "Physician assistants","Physical therapist assistants",
            "Software developers","Occupational therapy assistants",
            "Actuaries","Computer and information research scientists",
            "Operations research analysts","Solar photovoltaic installers",
            "Home health and personal care aides",
            "Personal care and service workers","Veterinary technologists and technicians"]


# Get jobs for all job titles in the job list
job_postings = []
for job_title in job_list:
    job_data = scrape_linkedin_jobs(job_title, "US", 1)
    job_postings.append(job_data)
    logging.info(f"Scraping for {job_title} is completed!")


# Create a dataframe full of the job listings
df = pd.concat([pd.DataFrame(job_data) for job_data in job_postings], ignore_index=True)
df.isna().sum()

df['salary'] = df['salary'].str.replace('Base pay range\n\n', '').str.strip()
df['salary'] = df['salary'].fillna('NA')
df['posted time'] = df['posted time'].fillna('NA')

# Fix format of description column
df["description"] = df["description"].str.replace(r"\n|Show more|Show less", "", regex=True)
df["description"] = df["description"].str.strip()

df.shape

df.head()

additional_samples_df = df.sample(50000, replace=True)
additional_samples_df.shape