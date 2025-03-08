import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL
BASE_URL = "https://www.randstad.com.sg/jobs/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
page_number = 1
jobs = []

while True:
    print(f"Scraping page {page_number}...")

    # Construct the page URL
    url = f"{BASE_URL}page-{page_number}"
    response = requests.get(url, headers=HEADERS)

    # Check for request failure
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_number}: {response.status_code}")
        break

    soup = BeautifulSoup(response.text, "html.parser")

    # Find job listing cards
    job_cards = soup.find_all("li", class_="cards__item")

    # If no job listings, stop scraping
    if not job_cards:
        print("No more job listings found. Stopping.")
        break

    for job in job_cards:
        try:
            title = job.find("h3", class_="cards__title").text.strip()

            # Extract job link
            link = "https://www.randstad.com.sg" + job.find("a", class_="cards__link")["href"]

            # Extract salary (if available)
            salary_text = None
            salary_li = job.find_all("li", class_="cards__meta-item")
            if len(salary_li) > 1:
                salary_text = salary_li[1].get_text(strip=True)

            # Extract job description
            description = job.find("div", class_="cards__description").text.strip()

            # Extract job posted date
            posted_date = job.find("span", class_="cards__date").text.strip()

            # Extract job type
            job_type = None
            job_type_element = job.find("li", class_="cards__meta-item")
            if job_type_element:
                job_type = job_type_element.text.strip()

            # Save the extracted data
            jobs.append({
                "Title": title,
                "Link": link,
                "Salary": salary_text,
                "Description": description,
                "Posted Date": posted_date,
                "Job Type": job_type
            })

        except AttributeError:
            print(f"Skipping a job entry due to missing data on page {page_number}")

    # Move to the next page
    page_number += 1
    time.sleep(2)  # Sleep to avoid hitting the server too fast

# Save to CSV
df = pd.DataFrame(jobs)
df.to_csv("jobs.csv", index=False)

print(f"Scraping complete. {len(jobs)} jobs saved to jobs.csv")
