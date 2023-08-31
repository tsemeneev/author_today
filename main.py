import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from utils import create_excel, add_data_to_excel


class Parser:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-lazy-loading')
        self.options.add_argument('--popup-blocking')

    def del_humanity_check(self):
        driver = webdriver.Chrome(options=self.options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Function;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            """
        })
        return driver

    def main(self):
        self.parse_popular()
        self.get_hot()
        self.get_bestseller()

    def parse_popular(self):
        driver = self.del_humanity_check()
        driver.maximize_window()
        driver.get('https://author.today/')

        listing = []
        for i in range(6):
            books = driver.find_element(By.ID, 'mostPopularWorks').find_element(
                By.CLASS_NAME, 'slick-track').find_elements(
                By.CLASS_NAME, 'book-cover-content ')
            for book in books:
                listing.append(book.get_attribute('href'))
            driver.find_element(By.XPATH, '//button[@aria-label="Next"]').click()
            time.sleep(1)
        self.parse_book_info('popular', list(set(listing)))
        driver.close()
        driver.quit()

    def get_hot(self):
        driver = self.del_humanity_check()
        driver.maximize_window()
        driver.get('https://author.today/')

        listing = []
        for i in range(6):
            books = driver.find_element(By.ID, 'hotWorks').find_element(
                By.CLASS_NAME, 'slick-track').find_elements(
                By.CLASS_NAME, 'book-cover-content ')

            for book in books:
                listing.append(book.get_attribute('href'))

            driver.find_elements(By.XPATH, '//button[@aria-label="Next"]')[1].click()
            time.sleep(1)
        self.parse_book_info('hot', list(set(listing)))
        driver.close()
        driver.quit()

    def get_bestseller(self):
        driver = self.del_humanity_check()
        driver.maximize_window()
        driver.get('https://author.today/')
        actions = webdriver.ActionChains(driver)
        actions.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
        listing = []
        for i in range(6):
            books = driver.find_element(By.ID, 'bestsellerWorks').find_element(
                By.CLASS_NAME, 'slick-track').find_elements(
                By.CLASS_NAME, 'book-cover-content ')
            for book in books:
                listing.append(book.get_attribute('href'))
            driver.find_elements(By.XPATH, '//button[@aria-label="Next"]')[3].click()
            time.sleep(1)
        self.parse_book_info('bestsellers', list(set(listing)))
        driver.close()
        driver.quit()

    def parse_book_info(self, category, links):
        create_excel(category)
        driver = self.del_humanity_check()
        driver.maximize_window()
        for link in links:
            driver.get(link)
            title = driver.find_element(By.XPATH, '//h1[@class="book-title"]').text
            author = driver.find_element(By.CLASS_NAME, 'book-authors').text
            genres = driver.find_element(By.CLASS_NAME, 'book-genres').text
            tags = driver.find_elements(By.CLASS_NAME, 'tags')
            if len(tags) == 0:
                tags = "Не указаны"
            else:
                tags = tags[0].find_elements(By.TAG_NAME, 'a')
                tags = ", ".join([tag.text for tag in tags][0:8])
            price = driver.find_elements(By.XPATH, '//span[@data-bind="html: priceText"]')
            if price[0].text == '':
                price = 'Цена не указана'
            else:
                price = price[0].text + 'Р'
            views = driver.find_element(By.CLASS_NAME, 'book-stats').find_element(
                By.XPATH, '//span[@class="hint-top-right"]').text
            likes = driver.find_element(By.CLASS_NAME, 'book-stats').find_element(
                By.XPATH, '//span[@class="like-count"]').text
            rewards = driver.find_element(By.XPATH, '//div[@class="col-xs-3"]').find_element(
                By.CLASS_NAME, 'panel-heading').find_elements(By.TAG_NAME, 'a')[1].text

            data = [[title, author, genres, tags, price, views, likes, rewards]]
            add_data_to_excel(data, category)


parser = Parser()
parser.main()
