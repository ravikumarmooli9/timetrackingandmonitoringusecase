from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TimeEntryViewSet, LeaveRequestViewSet, PredictTaskTimeView, ActivityMonitorView, TimeUtilizationView, LeaveRequestAutoApproveView, PredictTaskTimeMLView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'time-entries', TimeEntryViewSet)
router.register(r'leave-requests', LeaveRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('predict/', PredictTaskTimeView.as_view(), name='predict-task-time'),
    path('activity-monitor/', ActivityMonitorView.as_view(), name='activity-monitor'),
    path('time-utilization/', TimeUtilizationView.as_view(), name='time-utilization'),
    path('leave-auto/', LeaveRequestAutoApproveView.as_view(), name='leave-auto'),
    path('predict-ml/', PredictTaskTimeMLView.as_view(), name='predict-task-time-ml'),
]