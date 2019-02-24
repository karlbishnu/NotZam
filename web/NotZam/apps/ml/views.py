import os
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.utils.datastructures import MultiValueDict

# Create your views here.
from kafka import TopicPartition
from kafka.consumer.fetcher import ConsumerRecord

from common.log.logger import get_logger
from common.log.cid import get_cid
from common.model.model import get_model_summary
from common.mq.kafka import consumer, producer

logger = get_logger('notzam')


KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')

def home(request):
    return render(request, 'ml_home.html')


def model_summary(request: HttpRequest):
    return render(request, 'model_summary.html', {'model_summary': get_model_summary()})


from kafka import KafkaConsumer
c = KafkaConsumer(bootstrap_servers=KAFKA_BROKER_URL, group_id='test')
tp = TopicPartition('trained', 0)
c.assign([tp])

logger.info(KAFKA_BROKER_URL)


def training(request):
    if(request.is_ajax()):
        msg = c.poll(1)
        msg = _ext_latest_record_value(msg)
        c.seek_to_beginning()
        logger.info(msg)
        return JsonResponse({'echo': msg})

    send = producer(KAFKA_BROKER_URL)
    send('trainer', {'cid': get_cid()})
    return render(request, 'training.html')


def _ext_latest_record_value(msg):
    return json.loads(msg[tp][len(msg)-1].value) if len(msg) != 0 and len(msg[tp]) != 0 else '{}'


