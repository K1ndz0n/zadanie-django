from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["id"]

class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Task.history.model
        fields = "__all__"