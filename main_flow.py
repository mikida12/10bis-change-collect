from wrappers import webdriver_wrapper, email_wrapper
from time import sleep
from sites import ten_bis, segev
from utils import parse_config


if __name__ == "__main__":
    logger = parse_config.set_logger(file_name="output.txt", level="INFO")
    logger.info("starting...")

    config = parse_config.get_configurations(logger)
    daily_limit = config.get("daily_limit")

    web_driver_obj = webdriver_wrapper.WebDriverObject(config.get("browser"))

    used_today = ten_bis.get_balance_from_ten_bis(web_driver_obj, logger, config)
    transferred_success = False
    remaining_today = 0
    if used_today is not None and used_today is not False:
        remaining_today = daily_limit - used_today
        logger.info(f"remaining funds: {remaining_today}")
        sleep(3)

        if remaining_today > 0:
            transferred_success = segev.transfer_to_segev(web_driver_obj, remaining_today, logger, config)
        else:
            logger.info(f"insufficient funds. already used {used_today} NIS today")

    web_driver_obj.close_browser()
    logger.info("finished")

    email_wrapper.send_email(config, transferred_success, remaining_today)