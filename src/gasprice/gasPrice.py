import requests
import enum
import time
from config import TIMEOUT

requests.packages.urllib3.disable_warnings()

safe, propose, fast, suggest_base_fee = 'SafeGasPrice', 'ProposeGasPrice',\
                                        'FastGasPrice', 'suggestBaseFee'

# class GP_type(enum.Enum):
#     fast = 0
#     average = 1
#     slow = 2

class GP_type(enum.Enum):
    fast = 0
    average = 1
    slow = 2


class GP:

    @staticmethod
    def __get_gp():

        gp_data = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle",
                               verify=False).json()["result"]
        gp_data = {GP_type.fast.name: int(gp_data[fast]),
                   GP_type.average.name: int(gp_data[propose]),
                   GP_type.slow.name: int(gp_data[safe]),
                   suggest_base_fee: int(float(gp_data[suggest_base_fee]))}
        return gp_data

    @staticmethod
    def __get_eth_price():
        eth_price = \
            requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd').json()[
                'ethereum'][
                'usd']
        return float(eth_price)

    def __init__(self):
        self.eth_price = None
        self.gp_state = None
        self.update_gp()

    def update_gp(self):
        gp_data = None
        eth_price = None

        while not eth_price:
            try:
                eth_price = GP.__get_eth_price()
            except:
                pass
        self.eth_price = eth_price

        while not gp_data:
            try:
                gp_data = GP.__get_gp()
            except:
                pass

        self.gp_state = gp_data

def gp_updater(gp_data, eth_price):
    gp = GP()

    while True:
        gp.update_gp()
        for key in gp.gp_state.keys():
            gp_data[key] = gp.gp_state[key]
        eth_price.data = gp.eth_price
        print(gp_data, eth_price)
        time.sleep(TIMEOUT)
