from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from .models import Document
from .forms import DocumentForm

import logging
from cid.locals import get_cid

logger = logging.getLogger('uploads')

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
        logger.info(get_cid())
        logger.info(fs.path(filename))
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
