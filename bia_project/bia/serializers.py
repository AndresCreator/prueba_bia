from rest_framework import serializers
from bia.models import Bia


class BiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bia
        fields = ('id', 'active_energy', 'meter_date', 'meter_id')
