# conding: utf-8
import shutil, os
from django.conf import settings


def video_handel(file):
    path = os.path.join(settings.BASE_DIR, 'app/tmp/in')
    destination = open(os.path.join(path, file.name), 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()
