import json
import requests
from rich import print

# api_keys = [
#     'name',
#     'price',
#     'number_file',
#     'id_payment',
#     'body_contor',
#     'masraf_kol',
#     'payment_deadline',
#     'from_date',
#     'to_date',
# ]

def send_to_server(data):
    # data_json = json.dumps(data)
    # payload = {'json_payload': data_json, 'apikey': 'bs5aih@niu3@vyi4cr@iiuisj@fnrtsi@2323'}
    data['apikey'] = 'bs5aih@niu3@vyi4cr@iiuisj@fnrtsi@2323'

    # TODO exception handeling
    response = requests.post('http://baran.kavoshgaran.org/api/Electricity/Ticket/Create', data=data)
    # print("payload:", payload)

    print(response)

def process(data):
    result = {}
    splits = data.strip().splitlines()

    for l in splits:

        words = l.split(':')

        if l.__contains__('نام'):
            # name
            # print(words[1])

            result['name'] = words[1].strip()

        elif l.__contains__('مبلغ کل'):
            # #price
            # print(words[1])
            result['price'] = words[1].split()[0].strip()

        elif l.__contains__('پرونده'):
            # # number_file
            # # parvande has no colon
            # print(words[0].split()[-1])

            result['number_file'] = words[0].split()[-1].strip()

        elif l.__contains__('شناسه پرداخت'):
            # # id_payment
            # print(words[1])

            result['id_payment'] = words[1].strip()

        elif l.__contains__('شناسه قبض '):
            # # id_ticket
            # print(words[1])

            result['id_ticket'] = words[1].strip()

        elif l.__contains__('بدنه کنتور'):
            # # body_contor
            # print(words[1])

            result['body_contor'] = words[1].strip()

        elif l.__contains__('مصرف کل'):
            # #   masraf_kol
            # print(words[1])

            result['masraf_kol'] = words[1].strip()

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

        # # TODO add this too
        # # link_payment
        # print(splits[-1])
        elif l.__contains__('مشاهده و پرداخت قبض '):
            #result['payment_link'] = splits[-1].split('/')[-1]
            result['payment_link'] =splits[-1].strip()


    return result


if __name__ == '__main__':
    data = '''
    شرکت توزیع نیروی برق شمال کرمان
    نام : تست تستی 
    پرونده 87647
    بدنه کنتور : 6119401554853
    شناسه قبض : 1218678712123
    شناسه پرداخت : 660124555
    بدهي يا بستانکاري : 731 ريال 
    مبلغ کل : 3415911 ريال 
    مهلت پرداخت : 1400/01/30
    مصرف کل : 1200
    از : 1399/11/02
    تا : 1400/01/16
    مشاهده و پرداخت قبض 
    https://saapa.ir/b/125673736 
    '''

    # data2= {'name': 'somevalue',
    #         'number_file': 87647,
    #         'body_contor': 6119401554853,
    #         'id_ticket': 1218678712123,
    #         'id_payment': 660124555,
    #         'to_date': 1400/01/16,
    #         'price': 3415911,
    #         'payment_deadline': 1400/01/30,
    #         'masraf_kol': 1200,
    #         'from_date': 1399/11/02,
    #         'payment_link': 'https://saapa.ir/b/125673736'
    #         }

    data_to_post = process(data)

    print(data_to_post)

    send_to_server(data_to_post)
