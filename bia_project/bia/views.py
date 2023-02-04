from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from bia.models import Bia
from bia.serializers import BiaSerializer
from datetime import datetime, timedelta
import django_filters
from django_filters import rest_framework as filters
from django.db import models as django_models
from rest_framework.response import Response


# class EventFilter(filters.FilterSet):
#     class Meta:
#         model = Bia
#         fields = {
#             'meter_date': ('lte', 'gte')
#         }

#     filter_overrides = {
#         django_models.DateTimeField: {
#             'filter_class': django_filters.IsoDateTimeFilter
#         },
#     }

@api_view([ 'POST'])
def bia_list(request):
    print(request)
    
    if request.method == 'POST':
        data = JSONParser().parse(request)
        date = datetime.strptime(data["date"], '%Y-%m-%d')
        if(data["period"]=="daily"):
            t0, t1 = first_last_datetime_of_day(date)
        elif(data["period"]=="weekly"):
            t0, t1 = first_last_datetime_of_week(date)
        elif(data["period"]=="monthly"):
            t0, t1 = first_last_day_of_month(date)
        bia = Bia.objects.filter(meter_date__range=[t0, t1])

        bia = BiaSerializer(bia, many=True)
        return Response(bia.data)
    



def first_last_day_of_month(some_datetime):
    first_day = datetime(some_datetime.year, some_datetime.month, 1)
    last_day = datetime(some_datetime.year, some_datetime.month, 1) + timedelta(days=31)
    last_day = last_day.replace(day=1) - timedelta(days=1)
    return (first_day, last_day)

def first_last_datetime_of_day(some_datetime):
    first_datetime = datetime.combine(some_datetime.date(), datetime.min.time())
    last_datetime = datetime.combine(some_datetime.date(), datetime.max.time())
    return (first_datetime, last_datetime)

def first_last_datetime_of_week(some_datetime):
    first_datetime_of_week = some_datetime - timedelta(days=some_datetime.weekday())
    first_datetime_of_week = first_datetime_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    last_datetime_of_week = first_datetime_of_week + timedelta(days=6)
    last_datetime_of_week = last_datetime_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)
    return (first_datetime_of_week, last_datetime_of_week)