'''
Author MohammadMahdiOmid
Email:mohammadmehdiomid@gmail.com
'''

# imports
from __future__ import print_function
import logging
import time
from handling_sms import handleSms
from gsmmodem.modem import GsmModem

# every Port and Baudrate is different in any PC
PORT = "COM5"
BAUDRATE = 115200
PIN = None  # SIM card PIN (if any)


# initializing modem
def main():
    # while True:
    print('Initializing modem...')
    # To demonstrated our port and Baudrate
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    # created modem and recieving sms to proccessing
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    modem.smsTextMode = False
    # connect modem to PC
    modem.connect(PIN)
    print('Waiting for SMS message...')
    # To have delay for getting sms
    try:
        modem.rxThread.join(2 ** 20)
    finally:
        print("Trying from inside while loop")
        modem.close()


if __name__ == '__main__':
    # always run because it's server
    while True:
        try:
            print("Start...............................................................")
            logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
            main()
        except:
            time.sleep(5)
            print("Trying one more time")
            continue
