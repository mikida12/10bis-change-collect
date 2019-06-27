from wrappers import webdriver_wrapper, email_wrapper
from time import sleep
from sites import ten_bis, segev
from app import parse_config
from datetime import datetime


if __name__ == "__main__":
    logs_file = open("output.txt", "w")
    print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} starting...", file=logs_file)

    config = parse_config.get_configurations()
    daily_limit = config.get("daily_limit")

    web_driver_obj = webdriver_wrapper.WebDriverObject(config.get("browser"))

    used_today = ten_bis.get_balance_from_ten_bis(web_driver_obj, logs_file, config)
    remaining_today = daily_limit - used_today
    print(f"remaining funds: {remaining_today}", file=logs_file)
    sleep(3)

    if remaining_today > 0:
        segev.transfer_to_segev(web_driver_obj, remaining_today, logs_file, config)
    else:
        print(f"insufficient funds. already used {used_today} NIS today", file=logs_file)

    web_driver_obj.close_browser()

    print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} finished", file=logs_file)
    logs_file.close()

    email_wrapper.send_email(config)