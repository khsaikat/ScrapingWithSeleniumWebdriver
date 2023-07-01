from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


LINK = 'https://www.dkv-euroservice.com/DKVMaps/'
LOCATION = "Frankfurt"
AREA = 'Range: 10 km'

coordinates = []

options = Options()
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=options)

driver.get(LINK)

# Popup Button - Click
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()

# Search Bar - Type Location
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="isc_26"]'))).send_keys(LOCATION)

# Range - Dropdown Menu
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="isc_29"]'))).clear()
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="isc_29"]'))).send_keys(AREA)

# Find Button - Click
WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, "isc_21"))).click()

result_count = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, 'sstCount')))
result_count = int(result_count.text)

print("Number of Location: " + str(result_count))

# res = driver.find_elements(By.XPATH, '//*[@id="isc_9Atable"]/tbody/tr')
table = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="isc_9Atable"]')))

rows = WebDriverWait(table, 50).until(EC.presence_of_all_elements_located((By.XPATH, '//tr')))

driver.implicitly_wait(100)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

scrollbar = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, "scrollbar")))

print("Coordinates:")

for index in range(1, result_count+1):
    xpath_to_list_item = f'//*[@id="isc_9Atable"]/tbody/tr[{index}]/td[1]'
    xpath_to_list_item_index = f'//*[@id="isc_9Atable"]/tbody/tr[{index}]/td[1]/div'
    xpath_to_list_item_address = f'//*[@id="isc_9Atable"]/tbody/tr[{index}]/td[2]/div/div'

    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, xpath_to_list_item))).click()

    index = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, xpath_to_list_item_index)))
    address_full = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, xpath_to_list_item_address)))
    data = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, 'mapBalloonGeoposCoords')))

    lat_data = data.text.split(" ")[0]
    lon_data = data.text.split(" ")[2]
    print(index.text, lat_data, lon_data)

    coordinates.append([index.text, lat_data, lon_data, address_full.text])

    for scrolling in range(1, 6):
        WebDriverWait(scrollbar, 40).until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))[2].click()

df = pd.DataFrame(coordinates, columns=['Number', 'Latitude', 'Longitude', 'Address'])

df.to_csv('DKV Coords' + f'-{LOCATION}-{AREA.split(" ")[1]}km' + '.csv')

# driver.quit()
