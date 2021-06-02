import logging
import logging.config
import getHistorical
import datetime

logging.config.fileConfig('logging.conf')
logging.getLogger('fetcher')

TOP_TICKERS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT',
               'XRPUSDT', 'LTCUSDT', 'TRXUSDT']

# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w,
#                   1M

INTERVAL = '1h'

def main():
    currentDateTime = str(datetime.datetime.now())
    logging.info('Started at '+currentDateTime)
    print('Started at '+currentDateTime)
    for ticker in TOP_TICKERS:
        getHistorical.getTicker(ticker, INTERVAL)
    logging.info('Finished')


if __name__ == '__main__':
    main()
