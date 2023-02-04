from django.test import RequestFactory, TestCase
from rest_framework import status
from rest_framework.test import APITestCase
import datetime
from bia.models import Bia
from bia.serializers import BiaSerializer
from bia.views import bia_list

class BiaListTestCase(APITestCase):
    def setUp(self):
        # create instances of Bia model for testing
        Bia.objects.create(
            active_energy=10,
            meter_date=datetime.datetime(2022, 1, 1, 10, 0, 0),
            meter_id=1,
        )
        Bia.objects.create(
            active_energy=20,
            meter_date=datetime.datetime(2022, 1, 1, 11, 0, 0),
            meter_id=1,
        )
        Bia.objects.create(
            active_energy=30,
            meter_date=datetime.datetime(2022, 2, 1, 10, 0, 0),
            meter_id=1,
        )
        self.factory = RequestFactory()

    def test_daily_period(self):
        data = {
            "date": "2022-01-01",
            "period": "daily"
        }
        request = self.factory.post('/bia/list/', data, content_type='application/json')
        response = bia_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['meter_date'], "2022-01-01T10:00:00")
        self.assertEqual(response.data[0]['active_energy'], 10)
        self.assertEqual(response.data[1]['meter_date'], "2022-01-01T11:00:00")
        self.assertEqual(response.data[1]['active_energy'], 10)

    def test_weekly_period(self):
        data = {
            "date": "2022-01-01",
            "period": "weekly"
        }
        request = self.factory.post('/bia/list/', data, content_type='application/json')
        response = bia_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)
        self.assertEqual(response.data[0]['meter_date'], datetime.datetime.strptime("2021-12-27", "%Y-%m-%d"))
        self.assertEqual(response.data[0]['active_energy'], 0)
        self.assertEqual(response.data[1]['meter_date'], datetime.datetime.strptime("2021-12-28", "%Y-%m-%d"))
        self.assertEqual(response.data[1]['active_energy'], 0)
        self.assertEqual(response.data[2]['meter_date'], datetime.datetime.strptime("2021-12-29", "%Y-%m-%d"))
        self.assertEqual(response.data[2]['active_energy'], 0)
        self.assertEqual(response.data[3]['meter_date'], datetime.datetime.strptime("2021-12-30", "%Y-%m-%d"))
        self.assertEqual(response.data[3]['active_energy'], 0)
        self.assertEqual(response.data[4]['meter_date'], datetime.datetime.strptime("2021-12-31", "%Y-%m-%d"))
        self.assertEqual(response.data[4]['active_energy'], 0)
        self.assertEqual(response.data[5]['meter_date'], datetime.datetime.strptime("2022-01-01", "%Y-%m-%d"))
        self.assertEqual(response.data[5]['active_energy'], 10.0)
        self.assertEqual(response.data[6]['meter_date'], datetime.datetime.strptime("2022-01-02", "%Y-%m-%d"))
        self.assertEqual(response.data[6]['active_energy'], 0)


    def test_monthly_period(self):
        data = {
            "date": "2022-01-01",
            "period": "monthly"
        }
        request = self.factory.post('/bia/list/', data, content_type='application/json')
        response = bia_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 31)
        self.assertEqual(response.data[0]['meter_date'], datetime.datetime.strptime("2022-01-01", "%Y-%m-%d"))
        self.assertEqual(response.data[0]['active_energy'], 10.0)
        self.assertEqual(response.data[1]['meter_date'], datetime.datetime.strptime("2022-01-02", "%Y-%m-%d"))
        self.assertEqual(response.data[1]['active_energy'], 10.0)
