import time
import re
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to ChromeDriver
CHROMEDRIVER_PATH = r"C:\Users\Lotanna\Downloads\chromeDriver\chromedriver-win64\chromedriver.exe"

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Runs in the background

# Start WebDriver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the apprenticeship job listings page (1)
base_url = "https://www.findapprenticeship.service.gov.uk/apprenticeships?routeIds=7&sort=AgeAsc&levelIds=6&pageNumber="

page_number = 1 # Start from first page
apprenticeships = []  # Store apprenticeship details

while True:
    print(f"Scraping page {page_number}...")  # Debugging step

    # Navigate to the page
    driver.get(base_url + str(page_number))

    # Wait for apprenticeship listings to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "das-search-results__list-item"))
        )
    except:
        print("No more pages left or timeout reached")
        break # Exits the loop if no new listings are found

    # Find the parent container for all job listings
    apprenticeship_cards = driver.find_elements(By.CLASS_NAME, "das-search-results__list-item")

    if not apprenticeship_cards:
        print("No apprenticeship listings found on this page. Ending scrape.")
        break # If no listings are found, stop scraping

    print(f"Found {len(apprenticeship_cards)} apprenticeships on page {page_number}")  # Debugging step

    # Extract apprenticeship details
    for apprenticeship in apprenticeship_cards:
        try:
            # Extract job title (from <span> containing the title)
            title_element = apprenticeship.find_element(By.TAG_NAME, "span") 
            title = title_element.text.strip()
            title = title.replace("Digital Technology Solutions", "DTS").strip()
            title = title.replace("Digital & Technology Solutions", "DTS").strip()
            title = title.replace("Digital and Technology Solutions", "DTS").strip()
            title = title.replace("Digital Technologies Solutions", "DTS").strip()
            title = title.replace("Digital and technology solutions", "DTS").strip()
            title = title.replace("Application Production Services", "APS").strip()
            title = title.replace("Nuclear Software Engineering", "SWE").strip()
            title = title.replace("Software Engineering", "SWE").strip()

            # Employer name
            employer_element = apprenticeship.find_element(By.CLASS_NAME, "govuk-body")
            employer = employer_element.text.strip()

            # Location
            location_element = apprenticeship.find_elements(By.CLASS_NAME, "govuk-body")[1]  # Location is the second "govuk-body"
            location = location_element.text.strip()

            # Wage
            wage_element = apprenticeship.find_elements(By.CLASS_NAME, "govuk-body")[3]
            wage = wage_element.text.strip()

            # Remover the word 'Wage' from the string and extra spaces
            wage = wage_element.text.replace("Wage", "").replace("a year", "").strip()

            # Job link (the <a> tag)
            link_element = apprenticeship.find_element(By.CLASS_NAME, "das-search-results__link")
            apprenticeship_url = link_element.get_attribute("href")

            # Deadline
            try:
                deadline_element = apprenticeship.find_elements(By.CLASS_NAME, "govuk-body")[4]
                raw_deadline_text = deadline_element.text.strip()

                # Debugging: Print the extracted text from the website
                print(f"Raw Deadline Text: {raw_deadline_text}")

                # First, check if there is a date inside parentheses (Closes in X days (Monday 17 February))
                match = re.search(r'\((?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)?\s*(\d{1,2} [A-Za-z]+)\)', raw_deadline_text)

                if not match:
                    # If no parentheses format, extract date from "Closes on Monday 31 March 2025"
                    match = re.search(r'(?:Closes on )?(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)?\s*(\d{1,2} [A-Za-z]+)', raw_deadline_text)

                deadline = match.group(1) if match else "Not specified"

                print(f"Extracted Deadline: {deadline}")

            except Exception as e:
                deadline = "Not specified"
                print(f"Error: {e}")

            # Date Posted
            try:
                posted_element = apprenticeship.find_elements(By.CLASS_NAME, "govuk-body")[5]
                date_posted = posted_element.text.replace("Posted ", "").strip()
            except:
                date_posted = "Not specified"


            # Store apprenticeship details
            apprenticeships.append({
                "Title": title,
                "Employer": employer,
                "Location": location,
                "Wage": wage,
                "Deadline": deadline,
                "Posted": date_posted,
                "URL": apprenticeship_url
            })

        except Exception as e:
            print(f"Error extracting apprenticeship: {e}")
    
    # Check for "Next" button to stop when last page is reached
    try:
        next_button = driver.find_element(By.CLASS_NAME, "govuk-pagination__next")
    except:
        print("No 'Next' button found. Reached the last page.")
        break # Stops scraping when the last page is reached 

    # Move to the next page
    page_number += 1
    time.sleep(2)  # Short delay to avoid overwhelming the server

# Save to a CSV file
df = pd.DataFrame(apprenticeships) # Convert the list of dictionaries to a DataFrame
df.to_csv("vacancies.csv", index=False)  # Save as a CSV file

print("Scraping complete! Data saved to vacancies.csv")  # Debugging step

# Close the browser
driver.quit()
