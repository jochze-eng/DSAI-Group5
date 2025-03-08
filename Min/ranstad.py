import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

#URL = "https://www.randstad.com.sg/jobs/s-information-technology/"
URL = "https://www.randstad.com.sg/jobs/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
page_number = 1

response = requests.get("URL"+"page"+page_number, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

# Find all job listing cards
job_cards = soup.find_all("li", class_="cards__item")


jobs = []
for job in job_cards:
    # Extract Job Title
    title = job.find("h3", class_="cards__title").text.strip()

    # Extract Job Link (job details link)
    link = "https://www.randstad.com.sg" + job.find("a", class_="cards__link")["href"]

    # Extract Salary (starting with S$)
    salary_text = None
    salary_li = job.find_all("li", class_="cards__meta-item")
    if len(salary_li) > 1:  # Check if there's a second item (salary)
        salary_text = salary_li[1].get_text(strip=True)
    
    # Extract Job Description
    description = job.find("div", class_="cards__description").text.strip()

    # Extract Job Posted Date
    posted_date = job.find("span", class_="cards__date").text.strip()

    # Extract Job Type (permanent or contract)
    job_type = None
    job_type_element = job.find("li", class_="cards__meta-item")
    if job_type_element:
        job_type = job_type_element.text.strip()

    # Save the extracted data
    jobs.append({
        "Title": title,
        "Link": link,
        #"Salary Check": gg,
        "Salary": salary_text,
        "Description": description,
        "Posted Date": posted_date,
        "Job Type": job_type
    })

# Save to CSV or display
df = pd.DataFrame(jobs)
df.to_csv("jobs.csv", index=False)

# Optionally, print the results to check
#print(df)

with open("parsed_html.txt", "w", encoding="utf-8") as file:
    file.write(soup.prettify())

print("HTML content has been saved to 'parsed_html.txt'")
