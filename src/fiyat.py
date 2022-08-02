import datetime
import requests
import src.cfg as cfg

def get_current_data(update):

    x = datetime.datetime.now()
    date_clock = (x.strftime("%d/%m/%Y  %H:%M"))
    yanit = f'{date_clock}\n\n'

    for islem in cfg.İŞLEM_CİFTLERİ:
        url = f'https://api.binance.com/api/v3/avgPrice?symbol={islem}'  
        response = requests.get(url)
        data = response.json()
        data = float(data['price'])
        cevap = islem + " : " + str(round(data,3)) + "\n"
        yanit = f'{yanit} {cevap}'
    return yanit