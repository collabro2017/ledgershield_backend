# def getRates()

import json
import logging
import requests
from celery.schedules import crontab
from celery.task import task, periodic_task
from v1.coins.models import CoinPair



def fetch_pair_rate(pair):
    logger = logging.getLogger(__name__)
    url = 'https://shapeshift.io/marketinfo/{}'.format(pair)
    try:
        response = requests.get(url)
    except Exception as ex:
        logger.warning('Error while fetching rate of pair {}, {}'.format( pair, ex))
        return 500, None
    return response.status_code, response.text

@periodic_task(run_every=(crontab(minute='*/5')), name="sync_cp_rates", )
def sync_cp_rates():
    logger = logging.getLogger(__name__)
    paris = CoinPair.objects.all()
    for pair in paris:
        src = pair.source.symbol.lower();
        dst = pair.destination.symbol.lower();
        coin_pair = '{}_{}'.format(src,dst)
        # logger.info('https://shapeshift.io/marketinfo/{}'.format(coin_pair))
        status, data = fetch_pair_rate(coin_pair)
        if status == 200:
            market_info = json.loads(data)
            rate = market_info['rate']
            miner_fee = market_info['minerFee']
            pair.rate = rate
            pair.minerFee = miner_fee
            pair.save()
        logger.info('{} {}'.format(status, data))
