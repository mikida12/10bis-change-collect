from time import sleep
from utils import decorators


def calculate_load(total_sum):
    weights = [100, 50, 20, 10, 5, 1]
    index = 0
    return_dict = {}
    while int(total_sum) > 0:
        if total_sum >= weights[index]:
            return_dict[5 - index] = int(total_sum/weights[index])
            total_sum -= (int(total_sum/weights[index]) * weights[index])
        index += 1

    return return_dict


@decorators.retry()
def transfer_to_segev(web_driver_obj, amount_to_transfer, logger, configurations):
    # go to segev
    web_driver_obj.navigate_to_url("https://www.tabitorder.com/?site=598c22169debb722006d6d67#/app/order/menus")
    sleep(3)
    web_driver_obj.wait_for("//div[@class='hbox']//button")
    web_driver_obj.click_on("//div[@class='hbox']//button", "xpath")

    # click login
    web_driver_obj.wait_for("//a[@class='ng-binding dropdown-toggle']")
    web_driver_obj.click_on("//a[@class='ng-binding dropdown-toggle']")
    web_driver_obj.click_on("//ul[@class='dropdown-menu dropdown-menu-lg animated fadeInUp  pull-right with-arrow']//li[@role='menuitem'][1]")

    # fill credentials and submit
    web_driver_obj.type("//form//input[@type='email']", "xpath", configurations.get("output_funds").get("email"))
    web_driver_obj.type("//form//input[@type='password']", "xpath", configurations.get("output_funds").get("password"))
    web_driver_obj.click_on("//form//button")
    sleep(5)
    web_driver_obj.press_key("enter")

    web_driver_obj.wait_for("//div[@class='pull-right flip m-near-md pos-rlt text-xl ng-scope dropdown']//a//i")
    user_name = web_driver_obj.get_element_attribute("//div[@class='pull-right flip m-near-md pos-rlt text-xl ng-scope dropdown']//a//i", "xpath", "innerHTML").strip()
    logger.info(f"logged in to segev as {user_name}")
    sleep(3)

    # fill payment
    calculated_payment = calculate_load(amount_to_transfer)
    web_driver_obj.wait_for("//a[@class='hbox menulist-hbox ng-scope']")
    prefill_list = web_driver_obj.find_element_by("//a[@class='hbox menulist-hbox ng-scope']", "xpath", multi=True)
    for key, num_of_clicks in calculated_payment.items():
        prefill_list[key].click()
        # click +
        for i in range(1, num_of_clicks):
            web_driver_obj.click_on(
                "//div[@class='hbox text-lg']/div[@class='col cur-pointer text-center v-middle text-xl font-bold'][2]")
        # click 'add to cart'
        web_driver_obj.click_on("//button[@class='btn btn-lg btn-brand btn-block']")

    # check final amount
    total_amount = web_driver_obj.get_element_attribute("//span[@class='with-money ng-binding ng-scope']", "xpath", "innerHTML").strip("₪. 0")

    # assert that amount to be paid equals remaining funds
    assert int(total_amount) == int(amount_to_transfer), logger.error(f"Error! total amount {total_amount} not equals remaining funds {amount_to_transfer}")

    # click proceed to payment
    web_driver_obj.click_on("//button[@class='btn btn-brand btn-lg btn-block']")
    # get final amount again
    final_amount = web_driver_obj.get_element_attribute("//div[@class='m-t-xs font-balder ng-scope']//div[@class='pull-right flip ng-binding']", "xpath", "innerHTML").strip("₪. 0")
    assert int(total_amount) == int(final_amount), logger.error( f"Error! total amount {total_amount} not equals remaining funds {final_amount}")

    # click continue
    web_driver_obj.click_on("//button[@class='btn btn-lg btn-block btn-brand ng-binding']")

    # assert again
    paid_amount = web_driver_obj.get_element_attribute("//button[@class='btn btn-brand btn-lg btn-block']/span[2]", "xpath", "innerHTML").strip("₪. 0")
    assert int(total_amount) == int(paid_amount), logger.error(f"Error! total amount {total_amount} not equals remaining funds {paid_amount}")

    # pay -------->>>>>> click pay!
    web_driver_obj.click_on("//button[@class='btn btn-brand btn-lg btn-block']")
    sleep(10)

    web_driver_obj.wait_for("//div[@class='hbox desktop-offer-summary-title']/div[@class='col _value text-highlight text-far ng-binding']")
    total_paid = web_driver_obj.get_element_attribute("//div[@class='hbox desktop-offer-summary-title']/div[@class='col _value text-highlight text-far ng-binding']","xpath", "innerHTML").strip("₪. 0\n")
    assert int(total_paid) == int(amount_to_transfer), logger.error(f"Error! total amount paid {total_paid} not equals remaining funds {amount_to_transfer}")
    logger.info(f"successfully transferred {total_paid} NIS from 10bis to Segev!!!!!!!")

    return True