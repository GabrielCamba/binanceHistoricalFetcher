import os
import sys
import logging
import logging.config
import getHistorical
import datetime
from binance.client import Client
from dotenv import load_dotenv

logging.config.fileConfig('logging.conf')
logging.getLogger('fetcher')

load_dotenv()

api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

outputFolder = os.environ.get('output_folder')
if(outputFolder == None):
    logging.debug("Output folder not provided, setting default")
    outputFolder = './data/'
else:
    logging.debug("Output folder provided, setting "+outputFolder)

isdir = os.path.isdir(outputFolder)
if (not isdir):
    logging.error("NOT FOUND: Output folder "+outputFolder)
    sys.exit("ERROR: output folder "+outputFolder+" must exist, pĺease" \
             "create it or configure an output_folder in your .env file")

client = Client(api_key, api_secret)

with open('tickers') as f:
    tickers = f.read().splitlines()

with open('intervals') as f:
    intervals = f.read().splitlines()


def main():
    currentDateTime = str(datetime.datetime.now())
    logging.info('Started at '+currentDateTime)

    for ticker in tickers:
        for current in intervals:
            getHistorical.getTicker(client, ticker, current, outputFolder)

    logging.info('Finished')


if __name__ == '__main__':
    main()
