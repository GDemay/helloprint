# This is my readme

Blablabla

[]: # Language: markdown
[]: # Path: LICENSE


CRONTAB:


flask --app app/app.py crontab add


flask --app app/app.py crontab show
Currently active jobs in crontab:
80d5352791cf66871f31e8f33d16e9f0 -> app.app:scheduled_highest_price
40dc0602ae65b73518703d6fdb8ccee2 -> app.app:scheduled_lowest_price
f00d927b4ce94adf0e0da4a3b1ddeedd -> app.app:scheduled_median_price


flask --app app/app.py crontab run f00d927b4ce94adf0e0da4a3b1ddeedd


Improvement: 

Docker
Better tests
Better comments
