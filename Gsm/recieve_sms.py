from __future__ import print_function
import logging
import time
from gsmmodem.modem import GsmModem
from handle_sms import handleSms

LAST_TIME = time.time()
#It is different between computers
PORT = "COM7"
BAUDRATE = 115200
# SIM card PIN (if any)
PIN = None

def test():
    print("test....")

# initializing modem
def main():

    print('Initializing modem...')
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    modem.smsTextMode = False
    modem.connect(PIN)
    print('Waiting for SMS message...')
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
            time.sleep(2)
            print("Trying one more time")
            continue
