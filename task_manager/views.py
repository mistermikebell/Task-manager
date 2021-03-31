from django.shortcuts import render
from django.utils.translation import gettext


def index(request):
    context = {
        'title': gettext('Task manager')
    }
    return render(request, 'index.html', context)
