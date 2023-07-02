## Scrapping Website with Selenium Webdriver and Python

I am testing Selenium on a Map-based website. Here I used DKV Maps (https://www.dkv-euroservice.com/DKVMaps/)

## Built With

Frameworks/Libraries used in this project,

* [![Python][Python.shield]][Python-url]
* [![Selenium][Selenium.shield]][Selenium-url]
* [![Pandas][Pandas.shield]][Pandas-url]
* [![Google Chrome][GoogleChrome.shield]][GoogleChrome-url]



## Setup
1. Download the driver (chromedriver.exe) from [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/)
2. Add the driver (chromedriver.exe) to the project location
3. Run requirements.txt to install packages
   ```sh
   pip install -r requirements.txt
   ```
5. Replace the LOCATION variable in `main.py` with your desired location
6. Replace the AREA variable in `main.py` to change the search range (1, 5, 10, 20, 50)

## Result
The script will perform live scrapping and save data to CSV & JSON files at the end.


<!-- Links -->
[Python.shield]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[Selenium.shield]: https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white
[Selenium-url]: https://www.selenium.dev/
[Pandas.shield]: https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org/
[GoogleChrome.shield]: https://img.shields.io/badge/Google%20Chrome-4285F4?style=for-the-badge&logo=GoogleChrome&logoColor=white
[GoogleChrome-url]: https://chromedriver.chromium.org/


