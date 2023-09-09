import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from utils import create_excel, add_data_to_excel


class Parser:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('--headless')
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
        driver = self.del_humanity_check()
        driver.maximize_window()
        self.get_popular(driver)
        self.get_hot(driver)
        self.get_bestseller(driver)
        driver.close()
        driver.quit()

    def get_popular(self, driver):
        driver.get('https://author.today/')
        listing = []
        time.sleep(1)
        for i in range(6):
            books = driver.find_element(By.ID, 'mostPopularWorks').find_element(
                By.CLASS_NAME, 'slick-track').find_elements(
                By.CLASS_NAME, 'book-cover-content ')
            for book in books:
                listing.append(book.get_attribute('href'))
            driver.find_element(By.XPATH, '//button[@aria-label="Next"]').click()
            time.sleep(1)
        self.parse_book_info('popular', list(set(listing)), driver)

    def get_hot(self, driver):
        time.sleep(1)
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
        self.parse_book_info('hot', list(set(listing)), driver)

    def get_bestseller(self, driver):
        time.sleep(1)
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
        self.parse_book_info('bestsellers', list(set(listing)), driver)

    def parse_book_info(self, category, links, driver):
        create_excel(category)

        for link in links:
            driver.get(link)
            title = driver.find_element(By.XPATH, '//h1[@class="book-title"]').text
            author = driver.find_element(By.CLASS_NAME, 'book-authors').text
            genres = driver.find_element(By.CLASS_NAME, 'book-genres').find_elements(
                By.TAG_NAME, 'a')[1:]
            print(len(genres))
            try:
                genre_1 = genres[0].text
            except IndexError:
                genre_1 = 'Не указан'
            try:
                genre_2 = genres[1].text
            except IndexError:
                genre_2 = 'Не указан'
            try:
                genre_3 = genres[2].text
            except IndexError:
                genre_3 = 'Не указан'

            tags = driver.find_elements(By.CLASS_NAME, 'tags')
            if len(tags) > 0:
                tags = tags[0].find_elements(By.TAG_NAME, 'a')
                tag_list = get_tags(tags)
            else:
                tag_list = ['Не указан', 'Не указан', 'Не указан', 'Не указан',
                            'Не указан', 'Не указан', 'Не указан', 'Не указан']

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
                By.CLASS_NAME, 'panel-heading').find_elements(By.TAG_NAME, 'a')
            rewards = 'Нет наград' if len(rewards) < 2 else rewards[1].text

            data = [[title, author, price, views, likes, rewards, genre_1, genre_2, genre_3, tag_list[0],
                     tag_list[1], tag_list[2], tag_list[3], tag_list[4], tag_list[5], tag_list[6], tag_list[7]]]
            add_data_to_excel(data, category)


def get_tags(list_tags):
    try:
        tag_1 = list_tags[0].text
    except IndexError:
        tag_1 = 'Не указан'
    try:
        tag_2 = list_tags[1].text
    except IndexError:
        tag_2 = 'Не указан'
    try:
        tag_3 = list_tags[2].text
    except IndexError:
        tag_3 = 'Не указан'
    try:
        tag_4 = list_tags[3].text
    except IndexError:
        tag_4 = 'Не указан'
    try:
        tag_5 = list_tags[4].text
    except IndexError:
        tag_5 = 'Не указан'
    try:
        tag_6 = list_tags[5].text
    except IndexError:
        tag_6 = 'Не указан'
    try:
        tag_7 = list_tags[6].text
    except IndexError:
        tag_7 = 'Не указан'
    try:
        tag_8 = list_tags[7].text
    except IndexError:
        tag_8 = 'Не указан'

    return [tag_1, tag_2, tag_3, tag_4, tag_5, tag_6, tag_7, tag_8]


parser = Parser()
