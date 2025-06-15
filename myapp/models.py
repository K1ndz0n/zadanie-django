from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Task(models.Model):
    STATES = [
        ("new", "Nowy"),
        ("in_progress", "W toku"),
        ("finished", "Rozwiązany")
    ]

    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATES, default="new")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='tasks', null=True, blank=True)

    history = HistoricalRecords()