from __future__ import print_function
import logging
import time
from new_handle import handleSms
from gsmmodem.modem import GsmModem

LAST_TIME = time.time()

PORT = "COM5"
BAUDRATE = 115200
PIN = None  # SIM card PIN (if any)

# initializing modem
def main():
    # while True:
    print('Initializing modem...')
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    modem.smsTextMode = False
    modem.connect(PIN)
    print('Waiting for SMS message...')
    # thread = Thread(target=read_api)
    # thread.start()
    # thread2 = Thread(target=send_sms, args=(modem,))
    # thread2.start()
    try:
        modem.rxThread.join(2 ** 20)
    finally:
        print("Trying from inside while loop")
        modem.close()
if __name__ == '__main__':
    while True:
        try:
            print("Start...............................................................")
            logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
            main()
        except:
            time.sleep(5)
            print("Trying one more time")
            continue
