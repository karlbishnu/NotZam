from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from .models import Document
from .forms import DocumentForm

import logging
from cid.locals import get_cid

import json
from collections import OrderedDict

from NotZam.mq.message_queue import mq

logger = logging.getLogger('notzam')


def home(request):
    documents = Document.objects.all()
    return render(request, 'home.html', {'documents': documents})


def backgrounds(request):
    return save_file(request, 'backgrounds/')


def classes(request):
    return save_file(request)


def save_file(request, path=None):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name if path is None else path + myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        logger.info(fs.path(filename))

        make_json(fs.path(filename))
        return render(request, 'background_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'background_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {
        'form': form
    })


msg_q = mq("test")

import json
import os
from time import sleep

def serializer(m):
    return json.dumps(m).encode('utf-8')


from kafka import KafkaProducer, KafkaConsumer
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
#producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,
#                             value_serializer=lambda m: serializer(m))

print("Kafka producer of %s started" % KAFKA_BROKER_URL)

def make_json(path):
    jsondict = OrderedDict()
    jsondict["cid"] = get_cid()
    jsondict["path"] = path
    #producer.send('test', jsondict)
    #sleep(1)
    sent = msg_q(jsondict)
