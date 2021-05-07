from datetime import timedelta
import os
import logging
# here this is the name of the queue
listen = ['default']
log = logging.getLogger(__name__).setLevel(logging.CRITICAL)
logging.getLogger(__name__).propagate = False
logging.StreamHandler(stream=None)


def vaccine_condition(slot):
    if slot['min_age_limit'] <= MIN_AGE and slot['available_capacity'] > 0:
        return True
    else:
        return False


def check_for_medicine(candidates, date_range):
    from datetime import datetime
    import requests
    import json
    dates = [(datetime.now()+timedelta(days=i)).strftime('%d-%m-%Y') for i in range(0, date_range)]
    discord_link = 'https://discord.com/api/webhooks/840138751140823050/AIxtuanLipGckbvrYQxz99ft1nV1Bf5-AHbr0_QkklTDZzwstKC-MLna9YbR8mYCFVb_'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    co_win_url = 'https://api.cowin.gov.in/api/v2/appointment/sessions/public/findByPin'
    for candidate in candidates:
        output = ''
        for date in dates:
            pin_code = candidate['pin_code']
            name = candidate['name']
            url = f'{co_win_url}?pincode={pin_code}&date={date}'
            try:
                r = requests.get(url)
                res = r.json()
                sessions = res['sessions']
                valid_slots = list(filter(vaccine_condition, sessions))
                if len(valid_slots) > 0:
                    output += f'Vaccine status for {name} on {date} at pinCode: {pin_code}\n'
                    for slot in valid_slots:
                        name = slot['name']
                        address = slot['address']
                        vaccine = slot['vaccine']
                        slots = slot['slots']
                        fee = slot['fee']
                        dt = slot['date']
                        avl = slot['available_capacity']
                        output += f'name: {name}, address: {address}, vaccine: {vaccine}, slots: {slots}, fee: {fee}, date: {dt}, aval_capacity: {avl}\n'
            except Exception as e:
                print(e)
        if len(output) > 0:
            payload = {
                "content": output
            }
            payload = json.dumps(payload)
            requests.post(discord_link, data=payload, headers=headers)


MIN_AGE = 45

if __name__ == '__main__':
    import time
    while True:
        candidates = [
            {
                'name': 'Soni',
                'pin_code': '110092'
            },
            {
                'name': 'Atul',
                'pin_code': '110092'
            },
            {
                'name': 'Sweta',
                'pin_code': '110092'
            }
        ]
        date_range_check = 3
        check_for_medicine(candidates, date_range_check)
        # run in every 30 s
        time.sleep(15)
