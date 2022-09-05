# This is my readme


## Installation:

You must have Python3 and pip installed.

Create an environment with the following command:

```
python3 -m venv ~/.venv/bin/flask
source ~/.venv/bin/flask/bin/activate
```
Install flask:
```
sudo apt install python3-flask
```
Install the requirements:
```
pip install -r requirements.txt
```

Install Make

```
sudo apt install make
```




## Crontab:

In order to add the crontab, you must use this command:
```
flask --app app/app.py crontab add
```
```
(flask) (base) ➜  helloprint git:(1-create-a-crud) ✗ flask --app app/app.py crontab add
Adding cronjob: 80d5352791cf66871f31e8f33d16e9f0 -> app.app:scheduled_highest_price
Adding cronjob: 40dc0602ae65b73518703d6fdb8ccee2 -> app.app:scheduled_lowest_price
Adding cronjob: f00d927b4ce94adf0e0da4a3b1ddeedd -> app.app:scheduled_median_price
```
If you want to show the crontab, you must use this command:
```
flask --app app/app.py crontab show
Currently active jobs in crontab:
80d5352791cf66871f31e8f33d16e9f0 -> app.app:scheduled_highest_price
40dc0602ae65b73518703d6fdb8ccee2 -> app.app:scheduled_lowest_price
f00d927b4ce94adf0e0da4a3b1ddeedd -> app.app:scheduled_median_price
```
Running a specific job:
flask --app app/app.py crontab run 80d5352791cf66871f31e8f33d16e9f0

## Routes:
- GET SKU: /sku/<sku> # Get a SKU
è GET SKUs: /sku # Get all SKUs
- GET UPDATE_DATASET: /sku/update_dataset # Update the dataset
- GET BEST_SKU: /sku/best/ # Get the 5 highest SKY
- GET INCREASED_SKU: /sku/<sku>/ # Update by 21%
- POST CREATE_SKU: /sku/create # Create a SKU
- DELETE DELETE_SKU: /sku/<sku> # Delete a SKU
- LOWEST_SKU: /sku/lowest # Get the first SKU by Lowest price
- MEDIAN_SKU: /sku/median # Get the first SKU by Median price
- GET TIMEZONE: /timezone/<area>/<region> # Get the timezones from area or region

## Test:
```
make test
```
## Improvement: 

Docker
Better tests
Better comments
Better readme
