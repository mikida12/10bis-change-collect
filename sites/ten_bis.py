import re
from time import sleep
from utils import decorators


@decorators.retry()
def get_balance_from_ten_bis(web_driver_obj, logger, configurations):
    web_driver_obj.navigate_to_url("https://www.10bis.co.il")
    sleep(3)

    web_driver_obj.wait_for("//div[@class='styled__HeaderUserLink-sc-1s2hb09-4 bZLUPI'][2]")
    web_driver_obj.click_on("//div[@class='styled__HeaderUserLink-sc-1s2hb09-4 bZLUPI'][2]", "xpath")
    sleep(2)

    # login
    web_driver_obj.type("email", "id", configurations.get("input_funds").get("email"))
    web_driver_obj.type("password", "id", configurations.get("input_funds").get("password"))
    web_driver_obj.click_on("//button[@type='submit'][@class='styled__LongButton-sc-10wc8na-4 jxczNM']", "xpath")

    sleep(5)
    web_driver_obj.wait_for("//div[@class='styled__PrimaryText-sc-1snjgai-3 kjUIiq']")
    welcome_text = web_driver_obj.get_element_attribute("//div[@class='styled__PrimaryText-sc-1snjgai-3 kjUIiq']", "xpath", "innerHTML")
    logger.info(f"logged in to 10bis as - {welcome_text.split()[1]}")

    # open menu
    web_driver_obj.click_on("//img[@class='styled__MenuButtonImg-sc-1snjgai-7 cucpMo']", "xpath")
    # click to see funds
    web_driver_obj.wait_for("//div[@class='styled__ActionMenuLinksScrollContainer-sc-1snjgai-11 bNzFsl']//div[@class='styled__ActionMenuLinkContainer-sc-1snjgai-12 hHyZHL'][5]")
    web_driver_obj.click_on ("//div[@class='styled__ActionMenuLinksScrollContainer-sc-1snjgai-11 bNzFsl']//div[@class='styled__ActionMenuLinkContainer-sc-1snjgai-12 hHyZHL'][5]//div", "xpath")
    # get daily usage
    web_driver_obj.wait_for('//*[@id="__next"]/div/div[2]/div/div[3]/div[2]/div/div[3]/div/div')
    used_today = web_driver_obj.get_element_attribute('//*[@id="__next"]/div/div[2]/div/div[3]/div[2]/div/div[3]/div/div', "xpath", "innerHTML")
    used_today = int(re.findall(r'\d+', used_today)[0])
    logger.info(f"used today: {used_today}")

    return used_today
