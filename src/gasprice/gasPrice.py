import requests
import enum
import time
from config import TIMEOUT

requests.packages.urllib3.disable_warnings()


class GP_type(enum.Enum):
    fast = 0
    average = 1
    slow = 2


class GP:

    @staticmethod
    def __get_gp():

        gp_data = requests.get('https://www.gasnow.org/api/v2/gas/price', verify=False).json()['data']['list']
        gp_data = [round(gp_data[i]['gasPrice'] / 1000000000, 1) for i in range(4)]
        return gp_data

    @staticmethod
    def __get_eth_price():
        eth_price = \
            requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd').json()[
                'ethereum'][
                'usd']
        return float(eth_price)

    def __init__(self):
        gp_data = None
        eth_price = None

        while not gp_data:
            try:
                data = GP.__get_gp()
                gp_data = data if len(data) == 4 else None
            except:
                pass

        while not eth_price:
            try:
                eth_price = GP.__get_eth_price()
            except:
                pass

        self.__gp_snapshots_list = [gp_data]
        self.items = {
            'fastest': gp_data[0], 'fast': gp_data[1], 'standard': gp_data[2], 'slow': gp_data[3],
        }
        self.eth_price = eth_price

    def update_gp(self, gp_snapshots_list_len=4):
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
                data = GP.__get_gp()
                gp_data = data if len(data) == 4 else None
            except:
                pass

        if len(self.__gp_snapshots_list) < gp_snapshots_list_len:
            self.__gp_snapshots_list.append(gp_data)
        else:
            del self.__gp_snapshots_list[0]
            self.__gp_snapshots_list.append(gp_data)

        mid_minute_gp = [0, 0, 0, 0]
        for i in range(4):
            for gp in self.__gp_snapshots_list:
                mid_minute_gp[i] += gp[i]
            mid_minute_gp[i] = round(mid_minute_gp[i] / len(self.__gp_snapshots_list), 1)

        self.items['fastest'], self.items['fast'], self.items['standard'], self.items['slow'] = mid_minute_gp


def gp_updater(gp_data, eth_price):
    gp = GP()

    while True:
        gp.update_gp()
        for key in gp.items.keys():
            gp_data[key] = gp.items[key]
            eth_price.data = gp.eth_price
        time.sleep(TIMEOUT)
