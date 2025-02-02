import time
import pandas as pd
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
base_url = "https://www.findapprenticeship.service.gov.uk/apprenticeships?routeIds=7&sort=DistanceAsc&levelIds=6&pageNumber="

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
            wage = wage.replace("Wage", "").strip()

            # Job link (the <a> tag)
            link_element = apprenticeship.find_element(By.CLASS_NAME, "das-search-results__link")
            apprenticeship_url = link_element.get_attribute("href")

            # Store apprenticeship details
            apprenticeships.append({
                "Title": title,
                "Employer": employer,
                "Location": location,
                "Wage": wage,
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
