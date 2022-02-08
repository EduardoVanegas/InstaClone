
"""Django"""
from django.http.response import HttpResponse
"""Utilities"""
from datetime import date, datetime
import json

def hello_world(request):
    now=datetime.now().strftime('%b %dth, %Y - %H : %M hrs ')
    return HttpResponse(f'oh Hi, the current server time is: {now}')

def Sorted(request):
    numbers=[int(i) for i in request.GET['numbers'].split(',')]
    numbers_sort=sorted(numbers)
    data={
        'status':'ok',
        'numbers': numbers_sort,
        'message': 'Integers sorted succesfully.'
    }
    #import pdb; pdb.set_trace()
    return HttpResponse(
        json.dumps(data,indent=2),
        content_type="application/json"
        )

def say_hi(request,name,age):
    if age < 12:
        message = 'sorry {}, you are not allowed here'.format(name)
    else:
        message = 'Hello {}, you are welcome here'.format(name)
    return HttpResponse(message)