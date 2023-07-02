from selenium import webdriver
import pandas as pd
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# Link to the website
LINK = 'https://www.dkv-euroservice.com/DKVMaps/'
# Location of the search
LOCATION = "Bonn"
# Range of search (1, 5, 10, 20, 50)
AREA = 'Range: 5 km'

# This list is for CSV files. It will be best suited for conversion.
coordinates_list = []
# Alternatively, this list is for JSON files.
coordinates_list_2 = []

# Option to persist the CHROME browser and waiting for QUIT.
options = Options()
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=options)

# Here the web driver gets the visible data from the link.
driver.get(LINK)

# First Popup for accepting Cookies.
# Accept Button: Action performed -> Click
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()

# Search Bar at the top
# Action performed -> Type Location
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="isc_26"]'))).send_keys(LOCATION)

# Dropdown List for the Range of the search
# Action performed -> Clear data -> Type Range as the format shown in variable AREA
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="isc_29"]'))).clear()
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="isc_29"]'))).send_keys(AREA)

# Find Button beside the form
# Action performed -> Click
WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, "isc_21"))).click()

# Number of results
result_count = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, 'sstCount')))
result_count = int(result_count.text)

print("Number of Location: " + str(result_count))

# Search result in a Scrollable Table
table = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="isc_9Atable"]')))

# All the rows currently visible
rows = WebDriverWait(table, 50).until(EC.presence_of_all_elements_located((By.XPATH, '//tr')))

# Wait for the list to load
driver.implicitly_wait(100)

# Scroll down to page height for better access of the result Table
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Access Scrollbar to perform Scrolling
scrollbar = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, "scrollbar")))

print("Coordinates:")

# Collecting data while scrolling...
for index in range(1, result_count+1):
    xpath_to_list_item = f'//*[@id="isc_9Atable"]/tbody/tr[{index}]/td[1]'
    xpath_to_list_item_index = f'//*[@id="isc_9Atable"]/tbody/tr[{index}]/td[1]/div'
    xpath_to_list_item_address = f'//*[@id="isc_9Atable"]/tbody/tr[{index}]/td[2]/div/div'

    # Clicking Row from the result Table
    # Action performed -> Click
    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, xpath_to_list_item))).click()

    # Getting Row data and data from Popup window
    index = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, xpath_to_list_item_index)))
    address = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, xpath_to_list_item_address)))
    data = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, 'mapBalloonGeoposCoords')))

    # Cleaning the data
    lat_data = data.text.split(" ")[0]
    lon_data = data.text.split(" ")[2]
    address = address.text
    print(index.text, lat_data, lon_data)

    # Adding data to Lists
    coordinates_list.append([index.text, lat_data, lon_data, address])
    coordinates_list_2.append({'Number': index.text, 'Latitude': lat_data, 'Longitude': lon_data, 'Address': address})

    # For Scrolling down the Table
    # Action performed -> Click
    for scrolling in range(1, 6):
        WebDriverWait(scrollbar, 40).until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))[2].click()


# File location & name
file_name = './Scrapped Data/DKV Coords' + f'-{LOCATION}-{AREA.split(" ")[1]}km'

# Save data as CSV format
df = pd.DataFrame(coordinates_list, columns=['Number', 'Latitude', 'Longitude', 'Address'])
df.to_csv(file_name + '.csv')

# Save data as JSON format
with open(file_name + '.json', 'w') as outfile:
    json.dump(coordinates_list_2, outfile, indent=4)

# Close driver -> Close browser
# driver.quit()
