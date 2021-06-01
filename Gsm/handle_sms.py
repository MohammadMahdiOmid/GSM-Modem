import json
import requests
from datetime import datetime
from gsmmodem.modem import GsmModem, Sms
from gsmmodem.pdu import Concatenation
from threading import Thread
from api_retrieve import lock, shared_billing_id
import time
from rich import print
import persian

recieve_data = []
recieve_references = []
pre_references = None
pre_parts = 0


def send_sms(modem):
    while True:
        #TODO remove locks
        lock.acquire()

        try:
            if shared_billing_id:
                modem.sendSms('+989139935292', str(shared_billing_id))
                # sms._gsmModem.sendSms('+989139935292', str(shared_billing_id))
            else:
                print("Billing Id is null sleeping for 5 seconds")
                time.sleep(5)

        except:
            print("unable to sending sms")

        lock.release()


# connecting to server
def send_to_server(data):
    # data_json = json.dumps(data)
    # payload = {'json_payload': data_json, 'apikey': 'bs5aih@niu3@vyi4cr@iiuisj@fnrtsi@2323'}

    if data :
        # data['key'] = 'bs5aih@niu3@vyi4cr@iiuisj@fnrtsi@2323'
        try:
            response = requests.post('http://baran.kavoshgaran.org/api/Electricity/Ticket/Create', data=data)
            # print("payload:", payload)

            print(response)
            # print("response data is:",response.data)
        except:
            print('Excaption happned during POSTing data to the server')


def process(data):
    # data=data.strip()
    result = {}
    splits = data.strip().splitlines()
    data=persian.convert_ar_characters(data)

    #TODO recheck sms format

    # splits = data.strip().splitlines()
    sms_lines = data.splitlines()

    for l in sms_lines:

        words = l.split(':')

        if l.__contains__('نام'):
            # name
            # print(words[1])

            result['name'] = words[1].strip()

        elif l.__contains__('مبلغ کل'):
            # #price
            # print(words[1])
            result['price'] = int(words[1].split()[0].strip())

        elif l.__contains__('پرونده'):
            # # number_file
            # # parvande has no colon
            # print(words[0].split()[-1])

            result['number_file'] = int(words[0].split()[-1].strip())

        elif l.__contains__('شناسه پرداخت'):
            # # id_payment
            # print(words[1])

            result['id_payment'] =int(words[1].strip())

        elif l.__contains__('شناسه قبض '):
            # # id_ticket
            # print(words[1])

            result['id_ticket'] =int(words[1].strip())

        elif l.__contains__('بدنه کنتور'):
            # # body_contor
            # print(words[1])

            result['body_contor'] =int(words[1].strip())

        elif l.__contains__('مصرف کل'):
            # #   masraf_kol
            # print(words[1])

            result['masraf_kol'] =int(words[1].strip())

        elif l.__contains__('مهلت پرداخت'):
            # #   payment_deadline
            # print(words[1])

            result['payment_deadline'] = words[1].strip()

        elif l.__contains__('از'):
            # # from_date
            # print(words[1])

            result['from_date'] = words[1].strip()

        elif l.__contains__('تا'):
            # # to_date
            # print(words[1])

            result['to_date'] = words[1].strip()

        elif l.__contains__('مشاهده و پرداخت قبض'):
            # result['payment_link'] = splits[-1].split('/')[-1]
            result['link_payment'] =splits[-3].strip()

        # # TODO add this too
        # # link_payment
        # print(splits[-1])
    # for l in sms_lines:
    #     if l.startswith('htt'):
    #         print(l)
    #         result['payment_link'] = int(sms_lines[-1].split('/')[-1].strip())
    #         break
        result['key'] = 'bs5aih@niu3@vyi4cr@iiuisj@fnrtsi@2323'
    print("processing finish successefully")

    print(result)

    return result


def handleSms(sms):

    global pre_references
    global pre_parts
    global recieve_data
    global recieve_references

    if len(sms.udh) > 0:
        # print(len(sms.udh))
        reference = sms.udh[0].reference
        if reference in recieve_references:
            index = recieve_references.index(reference)
            recieve_data[index] += sms.text
            pre_parts -= 1

        else:
            recieve_references.append(reference)
            recieve_data.append(sms.text)
            pre_references = reference
            pre_parts = sms.udh[0].parts
            # already recieve one part
            pre_parts -= 1

    else:
        print(
            u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n'.format(sms.number, sms.time, sms.text))

        data = process(sms.text)

        # send_to_server(data)
        thread = Thread(target=send_to_server, args=(data,))
        thread.start()


    # printing long sms
    if pre_parts == 0:
        if pre_references:
            index = recieve_references.index(pre_references)

            print("number:")
            print(u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n'.format(sms.number, sms.time,
                                                                                              recieve_data[index]))

            data = process(recieve_data[index])

            thread = Thread(target=send_to_server, args=(data,))
            thread.start()
            # send_to_server(data)

        pre_references = None
        # freeing memory
        recieve_data = []
        recieve_references = []
