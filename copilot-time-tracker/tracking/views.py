from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Sum, F, ExpressionWrapper, DurationField
from drf_yasg.utils import swagger_auto_schema
from datetime import timedelta

from .models import Task, TimeEntry, LeaveRequest
from .serializers import (
    TaskSerializer, TimeEntrySerializer, LeaveRequestSerializer,
    PredictTaskTimeInputSerializer, PredictTaskTimeMLInputSerializer
)
from .ml import predict_task_time, predict_task_time_ml

User = get_user_model()

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TimeEntryViewSet(viewsets.ModelViewSet):
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer

    @action(detail=False, methods=['post'])
    def start(self, request):
        user = request.user
        task_id = request.data.get('task')
        if not task_id:
            return Response({'error': 'Task ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        # Optionally, check if there's already an open entry for this user/task
        entry = TimeEntry.objects.create(user=user, task=task, start_time=timezone.now(), end_time=None)
        serializer = self.get_serializer(entry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        try:
            entry = self.get_object()
        except TimeEntry.DoesNotExist:
            return Response({'error': 'Time entry not found.'}, status=status.HTTP_404_NOT_FOUND)
        if entry.end_time:
            return Response({'error': 'Time entry already stopped.'}, status=status.HTTP_400_BAD_REQUEST)
        entry.end_time = timezone.now()
        entry.save()
        serializer = self.get_serializer(entry)
        return Response(serializer.data)

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer

class PredictTaskTimeView(APIView):
    @swagger_auto_schema(request_body=PredictTaskTimeInputSerializer)
    def post(self, request):
        description = request.data.get('description', '')
        if not description:
            return Response({'error': 'Description is required.'}, status=status.HTTP_400_BAD_REQUEST)
        minutes = predict_task_time(description)
        hours = round(minutes / 60, 2)
        return Response({
            'predicted_minutes': minutes,
            'predicted_hours': hours
        })

class PredictTaskTimeMLView(APIView):
    @swagger_auto_schema(request_body=PredictTaskTimeMLInputSerializer)
    def post(self, request):
        features = request.data.get('features')
        if not features:
            return Response({'error': 'Features are required.'}, status=status.HTTP_400_BAD_REQUEST)
        predicted_time = predict_task_time_ml(features)
        predicted_hours = round(predicted_time / 60, 2)
        return Response({
            'predicted_minutes': predicted_time,
            'predicted_hours': predicted_hours
        })

class ActivityMonitorView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # Example: List users who worked more than 8 hours today
        today = timezone.now().date()
        overworked = (
            TimeEntry.objects
            .filter(start_time__date=today, end_time__isnull=False)
            .annotate(duration=ExpressionWrapper(F('end_time') - F('start_time'), output_field=DurationField()))
            .values('user')
            .annotate(total=Sum('duration'))
            .filter(total__gt=timezone.timedelta(hours=8))
        )
        result = []
        for entry in overworked:
            total_seconds = entry['total'].total_seconds()
            entry['total_hours'] = round(total_seconds / 3600, 2)
            result.append(entry)
        return Response(result)

class TimeUtilizationView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        period = request.query_params.get('period', 'all')  # daily, weekly, monthly, yearly, all
        now = timezone.now()

        if period == 'daily':
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
        elif period == 'weekly':
            start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=7)
        elif period == 'monthly':
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if start.month == 12:
                end = start.replace(year=start.year+1, month=1)
            else:
                end = start.replace(month=start.month+1)
        elif period == 'yearly':
            start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end = start.replace(year=start.year+1)
        else:  # all time
            start = None
            end = None

        qs = TimeEntry.objects.filter(end_time__isnull=False)
        if start and end:
            qs = qs.filter(start_time__gte=start, start_time__lt=end)

        utilization = (
            qs.annotate(duration=ExpressionWrapper(F('end_time') - F('start_time'), output_field=DurationField()))
            .values('user')
            .annotate(total=Sum('duration'))
        )
        result = []
        for entry in utilization:
            total_seconds = entry['total'].total_seconds()
            entry['total_hours'] = round(total_seconds / 3600, 2)
            result.append(entry)
        return Response(result)

class LeaveRequestAutoApproveView(APIView):
    serializer_class = LeaveRequestSerializer

    @swagger_auto_schema(request_body=LeaveRequestSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            start = serializer.validated_data['start_date']
            end = serializer.validated_data['end_date']
            conflict = LeaveRequest.objects.filter(user=user, start_date__lte=end, end_date__gte=start).exists()
            approved = not conflict
            leave = serializer.save()
            leave.approved = approved
            leave.save()
            return Response({'approved': approved, 'leave_id': leave.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
