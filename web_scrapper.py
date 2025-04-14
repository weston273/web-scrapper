import requests
from bs4 import BeautifulSoup

base_url = "https://vacancymail.co.zw"
jobs_url = f"{base_url}/jobs/"

# Set headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Send request
response = requests.get(jobs_url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Find all job listings
job_listings = soup.find_all("a", class_="job-listing")

# Loop through each job
for job in job_listings:
    title = job.find("h3", class_="job-listing-title").get_text(strip=True)
    description = job.find("p", class_="job-listing-text").get_text(strip=True)

    # Footer details (location, expiry, type, salary, posted)
    footer_items = job.find("div", class_="job-listing-footer").find_all("li")
    location = footer_items[0].get_text(strip=True) if len(footer_items) > 0 else "N/A"
    expires = footer_items[1].get_text(strip=True) if len(footer_items) > 1 else "N/A"
    job_type = footer_items[2].get_text(strip=True) if len(footer_items) > 2 else "N/A"
    salary = footer_items[3].get_text(strip=True) if len(footer_items) > 3 else "N/A"
    posted = footer_items[-1].get_text(strip=True)

    # Company logo (optional)
    logo_img = job.find("div", class_="job-listing-company-logo").find("img")
    logo_url = base_url + logo_img["src"] if logo_img else "No Logo"

    # Job detail link
    link = base_url + job["href"]

    # Display output
    print(f"Title: {title}")
    print(f"Description: {description}")
    print(f"Location: {location}")
    print(f"Expires: {expires}")
    print(f"Type: {job_type}")
    print(f"Salary: {salary}")
    print(f"Posted: {posted}")
    print(f"Logo URL: {logo_url}")
    print(f"Job Link: {link}")
    print("-" * 80)

#/////
import csv
import requests
from bs4 import BeautifulSoup

url = "https://vacancymail.co.zw/jobs/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all job listings
job_listings = soup.find_all('a', class_='job-listing')

# Prepare CSV
with open('scraped_jobs.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Job Title', 'Company', 'Location', 'Expiry', 'Job Type', 'Posted'])

    for job in job_listings:
        title = job.find('h3', class_='job-listing-title')
        title = title.text.strip() if title else 'N/A'

        company = job.find('div', class_='job-listing-company-logo')
        company_name = company.find('img')['alt'].strip() if company else 'N/A'

        details = job.find('div', class_='job-listing-footer')
        items = details.find_all('li') if details else []

        location = items[0].text.strip() if len(items) > 0 else 'N/A'
        expiry = items[1].text.strip() if len(items) > 1 else 'N/A'
        job_type = items[2].text.strip() if len(items) > 2 else 'N/A'
        posted = items[-1].text.strip() if len(items) > 3 else 'N/A'

        writer.writerow([title, company_name, location, expiry, job_type, posted])

print("✅ Job data saved to 'scraped_jobs.csv'")
