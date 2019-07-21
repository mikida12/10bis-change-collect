# 10bis-change-collect
Transfer remaining balance from TenBis card to external cards (currently Segev) automatically 

You can use this python project to transfer funds between 10bis card and Segev card (more options comning soon).


## Requirements

* Docker. No need for python, selenium or webdrivers.

## Run

* build a docker image. example: docker build --tag=tenbis-change .
* run the image. example: docker run --rm --shm-size 2g -v path/to/folder:/app  tenbis-change
