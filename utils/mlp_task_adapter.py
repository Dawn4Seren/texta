from time import sleep
import requests
import logging

class MLPTaskAdapter(object):

    def __init__(self, mlp_url, mlp_type='mlp'):
        self.start_task_url = '{0}/task/start/{1}'.format(mlp_url, mlp_type)
    
    def process(self, data):
        errors = {}
        started_task = requests.post(self.start_task_url, data=data).json()
        task_status_text = 'PENDING'

        while task_status_text == 'PENDING':
            sleep(10)
            task_status = requests.get(started_task['url']).json()
            task_status_text = task_status['status']

        analyzation_data = []

        if task_status_text == 'FAILURE':
            errors = {'task_failed': task_status}
            logging.error('Failed to analyze text with MLP Lite', extra={'url':self.start_task_url, 'texts': json.dumps(texts, ensure_ascii=False)})
        elif task_status_text == 'SUCCESS':
            analyzation_data = task_status['result']
        
        return analyzation_data, errors