"""Module for scraping Amazon category."""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, \
    ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class AmazonStat():
    """Class for getting data from amazon ads"""
    def __init__(self, url, target):
        self.target = target
        self.path = "C:/Program Files (x86)/chromedriver.exe"
        self.driver = webdriver.Chrome(self.path)
        self.driver.get(url)
        self.driver.maximize_window()

    def what_page(self):
        """Returns current page"""
        page = 0
        url = self.driver.current_url
        if url[-2] == "_":
            page = int(url[-1])
        elif url[-3] == "_":
            page = int(url[-2:])
        elif url[-4] == "_":
            page = int(url[-3:])
        return page

    def cookies_accept(self):
        """Cookies accept."""
        try:
            self.driver.find_element_by_id("sp-cc-accept").click()
        except NoSuchElementException:
            pass

    def next_page(self):
        """Gets next page"""
        self.cookies_accept()
        i = self.check_for_variieren()
        try:
            wait = WebDriverWait(self.driver, 3)
            xpath = ('//*[@id="search"]/div[1]/div[2]/div/span'
                     '[3]/div[2]/div[{}]/span/div/div/ul/li[9]'
                     '/a').format(str(36+i))
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
            try:
                wait = WebDriverWait(self.driver, 3)
                xpath = ('//*[@id="search"]/div[1]/div[2]/div/span'
                        '[3]/div[2]/div[{}]/span/div/div/ul/li[8]'
                        '/a').format(str(36 + i))
                wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
                try:
                    wait = WebDriverWait(self.driver, 3)
                    xpath = ('//*[@id="search"]/div[1]/div[2]/div/span'
                            '[3]/div[2]/div[{}]/span/div/div/ul/li[7]'
                            '/a').format(str(36 + i))
                    wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
                except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
                    pass

    def get_data(self):
        """Gets data from product table. Returns list of data."""
        data_list = []
        # Adding img url to data list
        try:
            img = self.driver.find_element_by_xpath(
                '//*[@id="landingImage"]')
            src = img.get_attribute('src')
            imgurl = ('=IMAGE("{}")').format(src)
            data_list.append(imgurl)
        except NoSuchElementException:
            data_list.append("No photo.")
        # Adding price to data list
        try:
            sprice = self.driver.find_element_by_xpath(
                '//*[@id="priceblock_ourprice"]').text
            price = float(sprice[:-5]+'.'+sprice[-4:-2])
            data_list.append(price)
        except NoSuchElementException:
            try:
                sprice = self.driver.find_element_by_xpath(
                    '//*[@id="priceblock_saleprice"]').text
                price = float(sprice[:-5]+'.'+sprice[-4:-2])
                data_list.append(price)
            except NoSuchElementException:
                try:
                    sprice = self.driver.find_element_by_xpath(
                        '//*[@id="priceblock_dealprice"]').text
                    price = float(sprice[:-5]+'.'+sprice[-4:-2])
                    data_list.append(price)
                except NoSuchElementException:
                    data_list.append("No price.")
        try:
            prod_info = self.driver.find_element_by_xpath(
                '//*[@id="productDetails_detailBullets_sections1"]/tbody').text
            # Adding ASIN to data list
            pos = prod_info.find('ASIN')
            if pos+1:
                asin = prod_info[pos+5:pos+15]
                data_list.append(asin)
            else:
                data_list.append("No ASIN")
            # Adiing buyers score to data list
            pos = prod_info.find('Kundenbewertung')
            if pos+1:
                buyers_rview_raw = prod_info[pos + 15:pos + 60]
                buyers_review = buyers_rview_raw[
                               buyers_rview_raw.find(' von') -
                               3:buyers_rview_raw.find(' von')]
                data_list.append(buyers_review)
            else:
                data_list.append("No Client Review")
            # Adding availability date to data list
            pos = prod_info.find('Im Angebot von Amazon.de seit')
            if pos+1:
                date_raw = prod_info[pos + 29:pos + 50]
                date = date_raw[1:date_raw.find('20', 5, 25) + 4]
                data_list.append(date)
            else:
                data_list.append("Unavailable")
            # Adding product rank to data list
            pos = prod_info.find('Rang')
            if pos:
                rank_info = prod_info[pos+4:pos+20]
                rank = rank_info[5:rank_info.find(' in')]
                try:
                    rank_to_int = int(rank[:-4] + rank[-3:])
                    data_list.append(float(rank_to_int))
                except ValueError:
                    data_list.append("Rank not available.")
            else:
                data_list.append("Rank not available")
        except NoSuchElementException:
            data_list = []

        return data_list

    def check_for_variieren(self):
        """Checks if notification exists"""
        try:
            self.driver.find_element_by_xpath(
                '//*[@id="search"]/div[1]/div[2]/div/span'
                '[3]/div[2]/div[2]/span/div/div/h1/span')
            correct = 1
        except NoSuchElementException:
            correct = 0
        return correct

    def prod_click(self, path_instance):
        """Clicks not sponsored add"""
        self.cookies_accept()
        increment = self.check_for_variieren()
        data = []
        try:
            wait = WebDriverWait(self.driver, 5)
            xpath = '//*[@id="search"]/div[1]/div[2]/div/span[3]' \
                    '/div[2]/div[{}]/div/span/div/div/div[2]/h2/' \
                    'a/span'.format(path_instance + increment)
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            data = self.get_data()
            self.driver.back()
        except (TimeoutException, ElementNotInteractableException):
            #print("Timed out. xPath: {} ProdClick()".format(xpath))
            pass
        return data

    def spons_prod_click(self, path_instance):
        """Clicks sponsored add"""
        self.cookies_accept()
        increment = self.check_for_variieren()
        data = []
        try:
            wait = WebDriverWait(self.driver, 5)
            xpath = '//*[@id="search"]/div[1]/div[2]/div/span[3]/' \
                    'div[2]/div[{}]/div/span/div/div/div/div/div[' \
                    '2]/h2/a/span'.format(path_instance + increment)
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            data = self.get_data()
            self.driver.back()
        except (TimeoutException, ElementNotInteractableException):
            #print("Timed out. xPath: {} SponsProdClick()".format(xpath))
            pass
        return data

    def quit(self):
        """Closes browser"""
        self.driver.quit()

