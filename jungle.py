import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


"""Module for checking estimates at Junglescout. Works only if you have Junglescout subscription."""


class CheckEstimate:
    """Checks estimated sales volume based on products sales rank."""
    def __init__(self):
        self.path = "C:/Program Files (x86)/chromedriver.exe"
        self.driver2 = webdriver.Chrome(self.path)
        self.driver2.get("https://www.junglescout.com/estimator/")
        self.driver2.maximize_window()
        self.driver2.find_element_by_xpath(
            '/html/body/div[2]/div[1]/main/section/div[2]/div[1]/div/div[1]'
            '/div[1]/div[3]/div[2]/div/span').click()
        time.sleep(1)
        self.driver2.find_element_by_xpath(
            '/html/body/div[2]/div[1]/main/section/div[2]/div[1]/div/div[1]'
            '/div[1]/div[3]/div[2]/div/ul/li[7]').click()
        self.driver2.find_element_by_xpath(
            '/html/body/div[2]/div[1]/main/section/div[2]/div[1]/div/div[1]'
            '/div[1]/div[4]/div[2]/div/span').click()
        time.sleep(1)
        self.driver2.find_element_by_xpath(
            '/html/body/div[2]/div[1]/main/section/div[2]/div[1]/div/div[1]'
            '/div[1]/div[4]/div[2]/div/ul/li[32]').click()

    def rank_input(self, rank):
        """Inputs rank of the product"""
        self.driver2.find_element_by_name('theRankInput').clear()
        enter_rank = self.driver2.find_element_by_name('theRankInput')
        enter_rank.send_keys(rank)
        enter_rank.send_keys(Keys.RETURN)
        time.sleep(2)
        estimate = self.driver2.find_element_by_xpath(
            '/html/body/div[2]/div[1]/main/section/div[2]'
            '/div[1]/div/div[1]/div[1]/div[1]/div[2]/p').text
        return estimate




