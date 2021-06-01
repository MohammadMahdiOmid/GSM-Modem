from __future__ import print_function
import logging
import time
from handle_sms import handleSms
from gsmmodem.modem import GsmModem
from threading import Thread
from handle_sms import send_sms
from api_retrieve import read_api

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
    while True:
        try:
            main()
        except:
            time.sleep(5)
            print("Trying one more time")
            continue
