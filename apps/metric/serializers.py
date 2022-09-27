from rest_framework import serializers
from .models import Metric

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'


class LogMetricSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    metric_id = MetricSerializer()
    hours = serializers.DateTimeField()