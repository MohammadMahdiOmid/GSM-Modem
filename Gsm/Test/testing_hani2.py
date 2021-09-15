from __future__ import print_function
import logging
import time
from Gsm.Test.testing_hani import handleSms , process
from gsmmodem.modem import GsmModem

# from handle_sms import send_sms
# from api_retrieve import read_api

# INDEX = 0
# CONTENT = ''
# NUMBER = '+989139935292'
LAST_TIME = time.time()

PORT = "COM5"
BAUDRATE = 115200
PIN = None  # SIM card PIN (if any)


def test():
    print("test....")


# initializing modem
def main():
    # while True:
    print('Initializing modem...')
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    modem.smsTextMode = False
    modem.connect(PIN)
    print('Waiting for SMS message...')
    #
    # thread = Thread(target=read_api)
    # thread.start()
    # thread2 = Thread(target=send_sms, args=(modem,))
    # thread2.start()

    try:
        test()
        modem.rxThread.join(2 ** 20)
    finally:
        print("Trying from inside while loop")
        modem.close()


if __name__ == '__main__':
    data = '''
شرکت توزیع نیروی برق شمال کرمان
نام : محسن ملا محمدي زاده نوقي
پرونده 39894
بدنه کنتور : 0
شناسه قبض : 1131729812120
شناسه پرداخت : 86300200
بدهي يا بستانکاري : 137 ريال 
مبلغ کل : 863138 ريال 
مهلت پرداخت : 1400/04/19
مصرف کل : 477000
از : 1400/02/25
تا : 1400/04/09
مشاهده و پرداخت قبض 
https://saapa.ir/b/113172981212
دانلود اپلیکشن برق من
https://saapa.ir/mobile-app
'''
    print(process(data))

    # while True:
    #     try:
    #         print("Start...............................................................")
    #         logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    #         main()
    #     except:
    #         time.sleep(5)
    #         print("Trying one more time")
    #         continue
