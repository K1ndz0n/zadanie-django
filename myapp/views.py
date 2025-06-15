from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Task
from .serializers import TaskSerializer, TaskHistorySerializer
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TaskFilter, TaskHistoryFilter

class CreateUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error: podaj wszystkie dane"}, status = 400)

        if User.objects.filter(username = username).exists():
            return Response({"error: login już istnieje"}, status = 400)

        user = User.objects.create_user(username = username, password = password)
        return Response({
            "id": user.id,
            "username": user.username
        })


class UserListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.all()
        result = []

        for user in users:
            result.append({
                "id" : user.id,
                "username" : user.username
            })

        return Response(result)


class CreateTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get("name")
        description = request.data.get("description", "")
        status = request.data.get("status", "new")
        user_id = request.data.get("user_id", None)

        if not name:
            return Response({"error: nie podano nazwy zadania"}, status = 400)

        if not User.objects.filter(id = user_id).exists():
            user_id = None

        valid_states = [state[0] for state in Task.STATES]
        if status not in valid_states:
            status = "new"

        task = Task.objects.create(
            name = name,
            description = description,
            status = status,
            user_id = user_id
        )

        if task.user:
            user_id = task.user.id

        return Response({
            "task_id" : task.id,
            "name" : task.name,
            "description" : task.description,
            "status" : task.status,
            "user_id" : user_id
        })

class EditTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk)

        name = request.data.get("name")
        description = request.data.get("description", "")
        status = request.data.get("status", "new")
        user_id = request.data.get("user_id", None)

        if not name:
            return Response({"error: nie podano nazwy zadania"}, status = 400)

        if not User.objects.filter(id = user_id).exists():
            user_id = None

        valid_states = [state[0] for state in Task.STATES]
        if status not in valid_states:
            status = "new"

        if (
                name == task.name and
                description == task.description and
                status == task.status and
                user_id == (task.user.id if task.user else None)
        ):
            return Response({"message": "Brak zmian."}, status=200)

        task.name = name
        task.description = description
        task.status = status
        task.user_id = user_id

        if task.user:
            user_id = task.user.id

        task.save()
        return Response({
            "task_id" : task.id,
            "name" : task.name,
            "description" : task.description,
            "status" : task.status,
            "user_id" : user_id
        })

    def patch(self, request, pk):
        task = get_object_or_404(Task, pk=pk)

        name = request.data.get("name", task.name)
        description = request.data.get("description", task.description)
        status = request.data.get("status", task.status)
        user_id = request.data.get("user_id", task.user_id)

        if not name:
            name = task.name

        if not User.objects.filter(id = user_id).exists():
            user_id = None

        valid_states = [state[0] for state in Task.STATES]
        if status not in valid_states:
            status = task.status

        if (
                name == task.name and
                description == task.description and
                status == task.status and
                user_id == (task.user.id if task.user else None)
        ):
            return Response({"message": "Brak zmian."}, status=200)

        task.name = name
        task.description = description
        task.status = status
        task.user_id = user_id

        if task.user:
            user_id = task.user.id

        task.save()
        return Response({
            "task_id": task.id,
            "name": task.name,
            "description": task.description,
            "status": task.status,
            "user_id": user_id
        })

    def delete(self, request, pk):
        user = request.user
        if not user.is_staff:
            return Response({"error" : "nie posiadasz wystarczających uprawnień"}, status = 403)

        task = get_object_or_404(Task, pk=pk)
        task.delete()

        return Response({"message" : "zadanie usunięte pomyślnie"}, status = 204)

class TaskInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        username = None
        if task.user:
            username = task.user.username

        return Response({
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "status": task.status,
            "user_id": task.user_id,
            "username": username
        })

class FilteredListView(ListAPIView):
    permission_classes = [AllowAny]

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

class FilteredHistoryView(ListAPIView):
    permission_classes = [AllowAny]

    queryset = Task.history.all()
    serializer_class = TaskHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskHistoryFilter