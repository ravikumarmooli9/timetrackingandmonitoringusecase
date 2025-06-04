from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task, TimeEntry, LeaveRequest

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'estimated_time']

class TimeEntrySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    duration = serializers.DurationField(read_only=True)

    class Meta:
        model = TimeEntry
        fields = ['id', 'user', 'task', 'start_time', 'end_time', 'duration']

class LeaveRequestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = LeaveRequest
        fields = ['id', 'user', 'start_date', 'end_date', 'reason']

class PredictTaskTimeInputSerializer(serializers.Serializer):
    description = serializers.CharField()

class PredictTaskTimeMLInputSerializer(serializers.Serializer):
    features = serializers.ListField(child=serializers.FloatField())