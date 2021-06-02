import os
import logging
from binance.client import Client
from binance.client import BinanceAPIException
from datetime import datetime
from pandas import pandas as pd
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

# following line is for being able to use the testnet api
# remove /api to access the website.
# pass de api_key and api_secret as parameters to the following call
client = Client(api_key, api_secret)
client.API_URL = 'https://testnet.binance.vision/api'

def millisToDateTimeString(millis):
    from_obj = datetime.fromtimestamp(millis/1000.0)
    return str(from_obj)

def getTicker(ticker_pair, interval):

    filename = 'data/'+ticker_pair+'.csv'

    logging.info('Processing '+ticker_pair+' on file: '+filename)

    try:
        df = pd.read_csv(filename)
        file_found = True
        stored_len = df.shape[0]
        logging.debug('csv len: '+str(stored_len))
    except FileNotFoundError as e:
        file_found = False
        logging.warn('File not found for pair: '+ticker_pair)
        logging.warn(e)

    try:
        earliest_available = client._get_earliest_valid_timestamp(ticker_pair,
                                                                  interval)
        earliest_available_s = millisToDateTimeString(earliest_available)
        logging.debug('earliest available api record: '+earliest_available_s)
    except BinanceAPIException as e:
        earliest_available = 0
        logging.error('there was a BinanceAPIException '+str(e.message))
        pass

    if(file_found and earliest_available):
        max_date = df['date'].max()
        max_date_s = millisToDateTimeString(max_date)
        logging.debug('latest register is: '+max_date_s)
        if(earliest_available > max_date):
            logging.warn('there will be a gap in the records between '
                         +max_date_s+' and '+earliest_available_s)
            from_date_to_fetch = earliest_available
        else:
            from_date_to_fetch = max_date
    else:
        from_date_to_fetch = earliest_available

    if from_date_to_fetch:
        bars = client.get_historical_klines(ticker_pair, '1h',
                                            str(from_date_to_fetch),
                                            limit=1000)
        new_df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low',
                                             'close', 'volume', 'close time',
                                             'qav', 'num of trades',
                                             'taker buy base asset vol',
                                             'take buy quote asset vol',
                                             'ignore'])

        length = new_df.shape[0]
        logging.info('Fetched data lenght: '+str(length))

        if(file_found):
            df = pd.concat([df, new_df])
        else:
            df = new_df

        # export DataFrame to csv
        logging.info('storing lines: '+str(df.shape[0])+
                     ' for ticker '+ticker_pair)
        df.to_csv(filename, index=False)
    else:
        logging.info('there was an error fetching data for ticker '+ticker_pair)

