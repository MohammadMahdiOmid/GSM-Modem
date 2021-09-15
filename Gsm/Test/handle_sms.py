import requests
from threading import Thread
from Gsm.Test.api_retrieve import lock, shared_billing_id
import time
from rich import print
import persian

#for sending messages
def send_sms(modem):
    while True:

        # TODO remove locks
        # creating lock to prevent message interference
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
    if data:

        try:
            response = requests.post('http://baran.kavoshgaran.org/api/Electricity/Ticket/Create', data=data)
            # To ckecking recieve data to server, we should print response and see response[200]
            print(response)

        except:
            print('Excaption happned during POSTing data to the server')

# To split data and processing the parts of the message we want to send to the server
def process(data):
    result = {}
    splits = data.strip().splitlines()
    data = persian.convert_ar_characters(data)

    # TODO recheck sms format
    sms_lines = data.splitlines()

    for l in sms_lines:

        words = l.split(':')

        if l.__contains__('نام'):
            result['name'] = words[1].strip()

        elif l.__contains__('مبلغ کل'):
            result['price'] = int(words[1].split()[0].strip())

        elif l.__contains__('پرونده'):
            result['number_file'] = int(words[0].split()[-1].strip())

        elif l.__contains__('شناسه پرداخت'):
            result['id_payment'] = int(words[1].strip())

        elif l.__contains__('شناسه قبض '):
            result['id_ticket'] = int(words[1].strip())

        elif l.__contains__('بدنه کنتور'):
            result['body_contor'] = int(words[1].strip())

        elif l.__contains__('مصرف کل'):
            result['masraf_kol'] = int(words[1].strip())

        elif l.__contains__('مهلت پرداخت'):
            result['payment_deadline'] = words[1].strip()

        elif l.__contains__('از'):
            result['from_date'] = words[1].strip()

        elif l.__contains__('تا'):
            result['to_date'] = words[1].strip()

        elif l.__contains__('مشاهده و پرداخت قبض'):
            # result['payment_link'] = splits[-1].split('/')[-1]
            result['link_payment'] = splits[-3].strip()

            # adding api_key
            result['key'] = 'bs5aih@niu3@vyi4cr@iiuisj@fnrtsi@2323'

        print("processing finish successefully")

        # printing data before sending to server
        print(result)

        # TODO add this too
        # link_payment
        # print(splits[-1])
        # for l in sms_lines:
        #  if l.startswith('htt'):
        #      print(l)
        #      result['payment_link'] = int(sms_lines[-1].split('/')[-1].strip())
        #      break
    return result


# To handle messages(some messages are short and some are long)
def handleSms(sms):
    global pre_references
    global pre_parts
    global recieve_data
    global recieve_references

    if len(sms.udh) > 0:
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
    # just printing details messages
    else:
        print(
            u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n'.format(sms.number, sms.time, sms.text))

        data = process(sms.text)

        # send_to_server(data) with another thread
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

            # send_to_server(data)
            thread = Thread(target=send_to_server, args=(data,))
            thread.start()

        pre_references = None
        # freeing memory
        recieve_data = []
        recieve_references = []
