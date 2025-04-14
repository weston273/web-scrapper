from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Step 1: Set up headless Chrome
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# Step 2: Start the browser and open the site
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://vacancymail.co.zw/jobs/")
time.sleep(5)  # Wait for JavaScript to load content

# Step 3: Parse page content with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Step 4: Close browser
driver.quit()

# Step 5: Find job postings
# You might need to update the class name based on what the site uses
job_listings = soup.find_all("div", class_="col-12 col-md-9")  # or a more specific container

# Step 6: Extract job data
jobs = []

for job in job_listings:
    title_tag = job.find("h5")
    if not title_tag:
        continue
    
    title = title_tag.get_text(strip=True)
    company_tag = title_tag.find_next("p")  # usually company name is in next <p>
    company = company_tag.get_text(strip=True) if company_tag else "N/A"
    
    info_text = job.get_text(" ", strip=True)
    location = "N/A"
    deadline = "N/A"

    if "Expires" in info_text:
        parts = info_text.split("Expires")
        if len(parts) > 1:
            deadline = parts[1].split()[0:3]
            deadline = " ".join(deadline)

    if "Harare" in info_text or "Mutare" in info_text or "Gokwe" in info_text:
        for city in ["Harare", "Mutare", "Gokwe"]:
            if city in info_text:
                location = city
                break

    jobs.append({
        "Job Title": title,
        "Company": company,
        "Location": location,
        "Expiry Date": deadline
    })

# Step 7: Display results
for i, job in enumerate(jobs[:10], 1):
    print(f"\nJob {i}")
    for k, v in job.items():
        print(f"{k}: {v}")
