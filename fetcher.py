import os
import logging
import logging.config
import getHistorical
import datetime
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()
# following line is for being able to use the testnet api
# remove /api to access the website.
# pass de api_key and api_secret as parameters to the following call

api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

client = Client(api_key, api_secret)
#client.API_URL = 'https://testnet.binance.vision/api'

logging.config.fileConfig('logging.conf')
logging.getLogger('fetcher')

TOP_TICKERS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT',
               'XRPUSDT', 'LTCUSDT', 'TRXUSDT']

# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w,
#                   1M
INTERVALS = ['1h', '4h', '1d']

def main():
    currentDateTime = str(datetime.datetime.now())
    logging.info('Started at '+currentDateTime)

    for ticker in TOP_TICKERS:
        for current in INTERVALS:
            getHistorical.getTicker(client, ticker, current)

    logging.info('Finished')


if __name__ == '__main__':
    main()
