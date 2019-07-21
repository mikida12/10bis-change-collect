# 10bis-change-collect
Transfer remaining balance from TenBis card to external cards (currently Segev) automatically 

You can use this python project to transfer funds between 10bis card and Segev card (more options conning soon).

Best use case is when you have a daily limit that "balances" to 0 every day, so you want to use entire available balance.
In the config file, enter your credentials to 10bis and Segev. If you want notifications by email, update your gmail credentials as well.
To completely automate the process, use a cron job like windows task scheduler or Linux crontab to excecute this script every day/week/month.

## Requirements 

* Docker. No need for python, selenium or webdrivers.

## Run

* build a docker image. example: docker build --tag=tenbis-change .
* run the image. example: docker run --rm --shm-size 2g -v path/to/folder:/app  tenbis-change
