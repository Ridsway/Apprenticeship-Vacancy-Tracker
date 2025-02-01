from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Path to ChromeDriver
CHROMEDRIVER_PATH = r"C:\Users\Lotanna\Downloads\chromeDriver\chromedriver-win64\chromedriver.exe"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Runs in the background

# Start WebDriver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the apprenticeship job listings page
url = "https://www.findapprenticeship.service.gov.uk/apprenticeships?sort=DistanceAsc&searchTerm=&location=&distance=10&levelIds=6&routeIds=7"
driver.get(url)

# Print page title to confirm we're on the right page
print("Page Title:", driver.title)

# Close the browser
driver.quit()