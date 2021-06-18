# Binance Historical Data Fetcher

This program aims to fetch information about asset pairs available in binance.com for analyizing and plot with another program

### Install and config

- Clone this repo
- Satisfy dependecies described on requirements.txt
- Copy .env.sample to .env
- Fill binance key and secret. [Here](https://binance.zendesk.com/hc/en-us/articles/360002502072-How-to-create-API) is described how to obtain them
- Change destination directory if you want to change default directory
- Change tickers file adding line by line the pairs you want to fetch. Use [this](https://api.binance.com/api/v3/exchangeInfo) endpoint to query valid ones.
- Change intervals file adding line by line one of the following options: *1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M*

Please notice **first time you run this program you'll be fetching all data available** for all the tickers by the intervals provided. This may take several time depending on the choices you have made. Use it at your own risk.
The following times the program will be completing available data based on last data feched. If there are gaps in your data we suggest to delete the file and run the program again.

### Usage

```BASH
python fetcher.py
```

You can customize this command in a cron job for fetching data periodically

### Output

- If everything worked as expected you'll find one csv file by ticker and interval in the data directory (or whatever is configured in .env file)
i.e: BTCUSDT_1h.csv

Columns:
```
date                      - Date fetched from the binance in ms
open                      - Open price
high                      - High price
low                       - Low price
close                     - Close price
volume                    - Volume operated
close time                - Close time in ms
qav                       - Quote asset volume
num of trades             - Number for trades
taker buy base asset vol  - Taker buy asset volume
take buy quote asset vol  - Taker buy quote asset volume	
ignore                    - Ignore
hrd                       - Human readable date (this is a conversion from the column date
```

EXPLAIN COLUMNS

- There's a log file in logs directory. If you want to debug there's more information of what had happened.
