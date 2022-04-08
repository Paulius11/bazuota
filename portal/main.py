from portal import Browser
from selenium.webdriver.common.by import By


# Press the green button in the gutter to run the script.
def local_run():
    browser = Browser()
    driver = browser.get_driver()
    driver.get(
        "https://www.skelbiu.lt/skelbimai/?autocompleted=1&keywords=&submit_bn=&cost_min=&cost_max=&type=0&condition=&cities=465&distance=0&mainCity=1&search=1&category_id=83&user_type=0&ad_since_min=0&ad_since_max=0&visited_page=1&orderBy=1&detailsSearch=0")
    print("test")
    skelbimu_sarasas = driver.find_element(By.XPATH, '//*[@id="itemsList"]/ul')
    skelbimas = skelbimu_sarasas.find_element(By.CLASS_NAME, 'simpleAds')
    print("Test")


if __name__ == '__main__':
    local_run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
