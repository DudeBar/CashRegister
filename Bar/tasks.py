from celery import task
from celery.utils.log import get_task_logger
import json
import requests

logger = get_task_logger(__name__)

@task()
def send_fidelity(products_list):
    for product in products_list:
        if product['id'] in ['2','4','6','9','10','94','97','98','110','111']:#les pintes
            product['type']="pinte"
        elif product['id'] in ['1','3','5','7','8','95','96','99']:#les demis
            product['type']="demi"
        elif product['id'] in ['14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34']:
            product['type']="bouteille"
        else:
            product['type']="autre"

    URL = 'http://www.dudebar.fr/add_command'
    params = dict(login="", password="", command=json.dumps(products_list))
    requests.post(URL, data=params, headers=dict(Referer=URL))