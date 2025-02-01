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

# Navigate to the apprenticeship job listings page
url = "https://www.findapprenticeship.service.gov.uk/apprenticeships?sort=DistanceAsc&searchTerm=&location=&distance=10&levelIds=6&routeIds=7"
driver.get(url)

# Wait for apprenticeship listings to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "das-search-results__list-item"))
)

# Find the parent container for all job listings
apprenticeship_cards = driver.find_elements(By.CLASS_NAME, "das-search-results__list-item")

print(f"Found {len(apprenticeship_cards)} apprenticeships")  # Debugging step

# Extract apprenticeship details
apprenticeships = []
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

# Print extracted apprenticeships
for apprenticeship in apprenticeships:
    print(apprenticeship)

# Close the browser
driver.quit()
