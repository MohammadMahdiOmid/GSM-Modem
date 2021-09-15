'''
Author MohammadMahdiOmid
Email:mohammadmehdiomid@gmail.com
'''

# imports
import time
import requests
from threading import Thread
from rich import print
import persian
from change_date import Persian, Gregorian

# for get sms and combine
recieve_data = []
recieve_references = []
pre_references = None
pre_parts = 0


# connecting to server
def send_to_server(data):
    # data_json = json.dumps(data)
    # payload = {'json_payload': data_json, 'apikey': 'bs5aih@niu3@vyi4cr@iiuisj@fnrtsi@2323'}

    # get data
    if data:
        # api key
        data['key'] = 'bs5aih@niu3@vyi4cr@iiuisj@fnrtsi@2323'
        try:
            # send post to server
            response = requests.post('http://baran.kavoshgaran.org/api/Electricity/Ticket/Create', data=data)
            # print("payload:", payload)

            print(response)
            print("response data is:", response.data)
        except:
            print('Excaption happned during POSTing data to the server')


def process(data):
    # prep for sending api
    result = {}
    # convert to good font(persian)
    data = persian.convert_ar_characters(data)

    # TODO recheck sms format

    # split every line
    sms_lines = data.splitlines()

    # to seprating every field for api
    for l in sms_lines:

        words = l.split(':')

        if l.startswith('نام'):

            result['name'] = words[1].strip()

        elif l.startswith('مبلغ کل'):

            result['price'] = int(words[1].split()[0].strip())

        elif l.startswith('پرونده'):

            result['number_file'] = int(words[0].split()[-1].strip())

        elif l.startswith('شناسه پرداخت'):

            result['id_payment'] = int(words[1].strip())

        elif l.startswith('شناسه قبض'):

            result['id_ticket'] = int(words[1].strip())

        elif l.startswith('بدنه کنتور'):

            result['body_contor'] = int(words[1].strip())

        elif l.startswith('مصرف کل'):

            result['masraf_kol'] = int(words[1].strip())

        elif l.startswith('مهلت پرداخت'):
            change_date = Persian(words[1].strip()).gregorian_string()

            result['payment_deadline'] = change_date

        elif l.startswith('از'):
            change_date = Persian(words[1].strip()).gregorian_string()

            result['from_date'] = change_date

        elif l.startswith('تا'):
            change_date = Persian(words[1].strip()).gregorian_string()

            result['to_date'] = change_date

        elif l.startswith('https://saapa.ir/b/'):

            result['payment_link'] = words[0].strip() + words[1].strip()

    print("processing finish successefully")
    print(result)
    return result


# get sms
def handleSms(sms):
    time.sleep(60)
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

        # prep sms to sending to server
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

            # send_to_server(data)
            thread = Thread(target=send_to_server, args=(data,))
            thread.start()

        pre_references = None
        # freeing memory
        recieve_data = []
        recieve_references = []
