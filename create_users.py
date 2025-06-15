import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zadanie.settings')
django.setup()

from django.contrib.auth.models import User

def create_default_users():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        print("Stworzono użytkownika admina")

    if not User.objects.filter(username='user').exists():
        User.objects.create_user('user', 'user@example.com', 'user')
        print("Stworzono zwykłego użytkownika")

if __name__ == '__main__':
    create_default_users()