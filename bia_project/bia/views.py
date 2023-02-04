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
from collections import defaultdict



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
    by_hour = False
    if request.method == 'POST':
        data = JSONParser().parse(request)
        date = datetime.strptime(data["date"], '%Y-%m-%d')
        if(data["period"]=="daily"):
            t0, t1 = first_last_datetime_of_day(date)
            by_hour=True
        elif(data["period"]=="weekly"):
            t0, t1 = first_last_datetime_of_week(date)
        elif(data["period"]=="monthly"):
            t0, t1 = first_last_day_of_month(date)
        bia = Bia.objects.filter(meter_date__range=[t0, t1]).order_by("meter_date")
        bia = BiaSerializer(bia, many=True)
        response = energy_difference(bia.data,by_hour)
        return Response(response)
    




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

def first_last_day_of_month(some_datetime):
    first_day = datetime(some_datetime.year, some_datetime.month, 1)
    last_day = datetime(some_datetime.year, some_datetime.month, 1) + timedelta(days=31)
    last_day = last_day.replace(day=1) - timedelta(days=1)
    return (first_day, last_day)

def energy_difference(data, by_hour=False):
    result = []
    diff_data = defaultdict(list)
    
    for item in data:
        date = datetime.strptime(item["meter_date"],"%Y-%m-%dT%H:%M:%SZ")
        diff_unit = date.replace(minute=0, second=0, microsecond=0)
        if not by_hour:
            diff_unit = diff_unit.replace(hour=0)
        diff_data[diff_unit].append(item['active_energy'])
    
    for diff_unit, energy_values in diff_data.items():
        result.append({
            'meter_date': diff_unit,
            'active_energy': energy_values[-1] - energy_values[0]
        })
        
    return result