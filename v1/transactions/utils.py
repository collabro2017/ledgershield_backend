from v1.coins.models import CoinPair


def get_pair_rates(src, dst):
    try:
        cp = CoinPair.objects.get(source__pk=src, destination__pk=dst)
        return  cp.rate
    except:
        return 0