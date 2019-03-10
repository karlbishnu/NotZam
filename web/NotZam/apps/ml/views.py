import os
import json

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.utils.datastructures import MultiValueDict

# Create your views here.
from kafka import TopicPartition

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


trained = consumer(KAFKA_BROKER_URL)
trained_partition = TopicPartition('trained', 0)
trained.assign([trained_partition])

detected = consumer(KAFKA_BROKER_URL)
detected_partition = TopicPartition('detected', 0)
detected.assign([detected_partition])

logger.info(KAFKA_BROKER_URL)


def training(request):
    if request.is_ajax():
        msg = trained.poll(1)
        msg = _ext_record_value(msg, trained_partition)
        logger.info(msg)
        return JsonResponse({'echo': msg})

    send = producer(KAFKA_BROKER_URL)
    send('trainer', {'cid': get_cid()})
    return render(request, 'ml_training.html')


def word_trigger(request):
    if request.is_ajax():
        msg = detected.poll(1)
        msg = _ext_record_value(msg, detected_partition)
        logger.info(msg)
        return JsonResponse({'detected': msg})

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        send = producer(KAFKA_BROKER_URL)
        send('detector', {'cid': get_cid(), 'filePath': fs.base_location+'/'+filename})
        return render(request, 'ml_word_trigger.html', {'reloaded': True})

    return render(request, 'ml_word_trigger.html')


def _ext_record_value(msg, partition):
    return msg[partition][len(msg) - 1].value if len(msg) != 0 and len(msg[partition]) != 0 else '{}'


