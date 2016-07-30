from django.http import HttpResponse
from django.template import loader

from .models import *


def index(request):
    template = loader.get_template('web/index.html')
    context = {
        'students': Student.objects.all()
    }
    return HttpResponse(template.render(context, request))