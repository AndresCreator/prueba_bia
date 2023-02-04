from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from bia.models import Bia
from bia.serializers import BiaSerializer
from datetime import datetime, timedelta
from rest_framework.response import Response
from collections import defaultdict
import calendar




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
            bia = get_bia(t0,t1)
            response = energy_diff_by_hour(bia)
            return Response(response)
        if(data["period"]=="weekly"):
            t0, t1 = first_last_datetime_of_week(date)
            bia = get_bia(t0,t1)
            response = energy_diff_by_week(bia,date)
            return Response(response)
        if(data["period"]=="monthly"):
            t0, t1 = first_last_day_of_month(date)
            bia = get_bia(t0,t1)
            response = energy_diff_by_month(bia,date)
            return Response(response)

        
    

def get_bia(t0,t1):
    bia = Bia.objects.filter(meter_date__range=[t0, t1]).order_by("meter_date")
    return BiaSerializer(bia, many=True).data


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



def energy_diff_by_hour(data):
    result = []
    diff_data = defaultdict(list)
    
    for item in data:
        date  = datetime.strptime(item["meter_date"],"%Y-%m-%dT%H:%M:%SZ")
        diff_unit = date.replace(minute=0, second=0, microsecond=0)
        diff_data[diff_unit].append(item['active_energy'])
    
    for diff_unit, energy_values in diff_data.items():
        result.append({
            'meter_date': diff_unit,
            'active_energy': energy_values[-1] - energy_values[0]
        })
        
    return result

def _energy_diff_by_time_unit(data, time_unit, start, end, step):
    result = []
    diff_data = defaultdict(list)
    
    for item in data:
        date  = datetime.strptime(item["meter_date"],"%Y-%m-%dT%H:%M:%SZ")
        diff_unit = date.replace(minute=0, second=0, microsecond=0, hour=0)
        diff_data[diff_unit].append(item['active_energy'])
    
    for i in range((end - start).days + 1):
        diff_unit = start + timedelta(days=i)
        if diff_unit in diff_data:
            result.append({
                'meter_date': diff_unit,
                'active_energy': diff_data[diff_unit][-1] - diff_data[diff_unit][0]
            })
        else:
            result.append({
                'meter_date': diff_unit,
                'active_energy': 0
            })
    return result

def energy_diff_by_month(data, month):
    num_days = calendar.monthrange(month.year, month.month)[1]
    start = datetime(month.year, month.month, 1)
    end = datetime(month.year, month.month, num_days)
    
    return _energy_diff_by_time_unit(data, 'month', start, end, timedelta(days=1))

def energy_diff_by_week(data, week):
    week_start = week - timedelta(days=week.weekday())
    week_end = week_start + timedelta(days=6)
    
    return _energy_diff_by_time_unit(data, 'week', week_start, week_end, timedelta(days=1))


