from threading import Thread, Lock
import requests

lock = Lock()
shared_billing_id = None
previes_id = -1

def read_api():
    global shared_billing_id
    global previes_id

    while True:
        try:

            data = requests.get("https:")

            if data:

                # TODO recheck api key
                id = data.get('billing_id')
                lock.acquire()
                if id == previes_id:
                    # making shared billing id none so that repeatative smses are not send to Edareh bargh
                    shared_billing_id = None
                else:
                    shared_billing_id = id
                    previes_id = id

                lock.release()
        except:
            pass
            # print("api unreachable")
