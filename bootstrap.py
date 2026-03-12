import os
from pathlib import Path

structure = {
    "requirements.txt": """Django>=5.0
mysqlclient
SpeechRecognition
pydub
ffmpeg-python
groq
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
requests
python-dotenv
""",
    ".env": """SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=meetings_ai
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306

GROQ_API_KEY=your-groq-api-key
TRELLO_API_KEY=your-trello-api-key
""",
    "manage.py": """#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
""",
    "config/__init__.py": "",
    "config/settings.py": """import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.users',
    'apps.meetings',
    'apps.email_ai',
    'apps.tasks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'meetings_ai'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
""",
    "config/urls.py": """from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('meetings/', include('apps.meetings.urls')),
    path('email/', include('apps.email_ai.urls')),
]
""",
    "apps/__init__.py": "",
    "apps/users/__init__.py": "",
    "apps/users/apps.py": """from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
""",
    "apps/users/models.py": """from django.db import models
from django.contrib.auth.models import User

# Using Django's built-in User model.
""",
    "apps/users/views.py": """from django.shortcuts import render

# Authentication views go here.
""",
    "apps/users/urls.py": """from django.urls import path
from . import views

urlpatterns = [
    # path('login/', views.login_view, name='login'),
]
""",
    "apps/meetings/__init__.py": "",
    "apps/meetings/apps.py": """from django.apps import AppConfig

class MeetingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.meetings'
""",
    "apps/meetings/models.py": """from django.db import models
from django.contrib.auth.models import User

class Meeting(models.fields.related.ForeignKey):
    # wait, fixing the bad skeleton from earlier thought
    pass
""",
}

# Real models.py content for meetings
structure["apps/meetings/models.py"] = """from django.db import models
from django.contrib.auth.models import User

class Meeting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    input_type = models.CharField(max_length=50) # e.g., 'audio', 'text', 'manual'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
"""

structure["apps/tasks/__init__.py"] = ""
structure["apps/tasks/apps.py"] = """from django.apps import AppConfig

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tasks'
"""
structure["apps/tasks/models.py"] = """from django.db import models
from apps.meetings.models import Meeting
from django.contrib.auth.models import User

class ActionItem(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='action_items')
    task = models.TextField()
    owner = models.CharField(max_length=255)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    trello_synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task} - {self.priority}"

class TrelloCredential(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    list_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Trello Credentials for {self.user.username}"
"""

structure["apps/email_ai/__init__.py"] = ""
structure["apps/email_ai/apps.py"] = """from django.apps import AppConfig

class EmailAiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.email_ai'
"""
structure["apps/email_ai/models.py"] = """from django.db import models
from django.contrib.auth.models import User

class GmailCredential(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_expiry = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Gmail Credentials for {self.user.username}"
"""

structure["apps/meetings/views.py"] = """from django.shortcuts import render

def meeting_list(request):
    # Return list of meetings
    return render(request, 'meetings/list.html')
"""
structure["apps/meetings/urls.py"] = """from django.urls import path
from . import views

urlpatterns = [
    path('', views.meeting_list, name='meeting_list'),
]
"""

structure["apps/email_ai/views.py"] = """from django.shortcuts import render

def email_dashboard(request):
    # Email AI dashboard
    return render(request, 'email_ai/dashboard.html')
"""
structure["apps/email_ai/urls.py"] = """from django.urls import path
from . import views

urlpatterns = [
    path('', views.email_dashboard, name='email_dashboard'),
]
"""

structure["apps/meetings/services/__init__.py"] = ""
structure[
    "apps/meetings/services/audio_processing.py"
] = """# Handles conversion from Audio to Text
import speech_recognition as sr
from pydub import AudioSegment

def convert_audio_to_text(file_path):
    # Placeholder for audio processing logic using speech_recognition and pydub
    pass
"""
structure[
    "apps/meetings/services/meeting_pipeline.py"
] = """# Orchestrates meeting processing flow
from apps.ai_engine.meetings_ai_engine import process_meeting_text

def run_meeting_pipeline(meeting_input, input_type):
    # Placeholder for orchestrating speech-to-text -> AI Engine -> Save to DB
    pass
"""

structure["apps/email_ai/services/__init__.py"] = ""
structure[
    "apps/email_ai/services/gmail_auth.py"
] = """# Handles OAuth2 integration with Gmail API

def authenticate_gmail(user):
    # Placeholder for OAuth2 flow
    pass
"""
structure[
    "apps/email_ai/services/gmail_reader.py"
] = """# Handles reading emails from Gmail API

def fetch_recent_emails(user, count=10):
    # Placeholder for fetching emails
    pass
"""
structure[
    "apps/email_ai/services/gmail_sender.py"
] = """# Handles sending emails via Gmail API

def send_email(user, to_address, subject, body):
    # Placeholder for sending emails
    pass
"""

structure["apps/ai_engine/__init__.py"] = ""
structure["apps/ai_engine/groq_client.py"] = """# Centralized client for Groq API
import os
from groq import Groq

def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    return Groq(api_key=api_key)
"""
structure[
    "apps/ai_engine/meetings_ai_engine.py"
] = """# Handles AI reasoning for meetings
from .groq_client import get_groq_client

def process_meeting_text(text):
    # Uses Groq LLaMA to generate Summary, Tasks, and High Priority Tasks
    # Do NOT implement full prompt yet. Returns a structured dict.
    pass
"""
structure["apps/ai_engine/email_ai_engine.py"] = """# Handles AI reasoning for emails
from .groq_client import get_groq_client

def analyze_email_content(email_text, action):
    # Handles asking questions, summarizing, or drafting replies using LLM
    pass
"""

structure["apps/tasks/services/__init__.py"] = ""
structure[
    "apps/tasks/services/trello_client.py"
] = """# Handles API integration with Trello

def sync_task_to_trello(user, task_data):
    # Placeholder for syncing an ActionItem to Trello
    pass
"""

structure["templates/base.html"] = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meetings & Productivity AI</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Meetings AI</a>
        </div>
    </nav>
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{% static 'js/main.js' %}"></script>
</body>
</html>
"""
structure["templates/dashboard.html"] = """{% extends 'base.html' %}
{% block content %}
<h2>Dashboard</h2>
<p>Welcome to Meetings & Productivity AI.</p>
{% endblock %}
"""
structure["templates/meetings/list.html"] = """{% extends 'base.html' %}
{% block content %}
<h2>Your Meetings</h2>
<!-- Placeholder for meetings list -->
{% endblock %}
"""
structure["templates/email_ai/dashboard.html"] = """{% extends 'base.html' %}
{% block content %}
<h2>Email AI Dashboard</h2>
<!-- Placeholder for email tools -->
{% endblock %}
"""

structure["static/css/style.css"] = """/* Minimal custom CSS */
body {
    background-color: #f8f9fa;
}
"""
structure["static/js/main.js"] = """/* Minimal JavaScript */
console.log("Meetings AI loaded.");
"""

for filepath, content in structure.items():
    dir_name = os.path.dirname(filepath)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Skeleton generated successfully.")
