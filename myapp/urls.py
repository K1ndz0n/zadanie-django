from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import CreateUserView, CreateTaskView, UserListView, EditTaskView, TaskInfoView, FilteredListView, FilteredHistoryView

urlpatterns = [
    path('api/login/', obtain_auth_token),
    path('api/register/', CreateUserView.as_view(), name = "register"),
    path('api/task/create/', CreateTaskView.as_view(), name = "create-task"),
    path('api/user-list/', UserListView.as_view(), name = "user-list"),
    path('api/task/edit/<int:pk>/', EditTaskView.as_view(), name = "edit-task"),
    path('api/task/info/<int:pk>/', TaskInfoView.as_view(), name = "task-info"),
    path('api/tasks/', FilteredListView.as_view(), name = "task-list"),
    path('api/history/', FilteredHistoryView.as_view(), name = "history")
]