from django.conf.urls import url

from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout
from django.contrib.auth import views as auth_views
from django.conf.urls import include

from . import forms
from . import views

urlpatterns = [
    url(r"^main/", views.MainView.as_view()),
    url(
        r"^login/",
        login,
        {"template_name": "login.html", "authentication_form": forms.LoginForm},
        name="login",
    ),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r"^logout/$", logout, {"next_page": "/exit"}, name="logout"),
    url(r"^new/", TemplateView.as_view(template_name="feedback/new_form.html")),
    url(r"^exit/", views.exit_view),
    url(r"^done_cron/(?P<dept_name>[\w\-]+)$", views.done_cron),
    url(r"^done", views.done_view),
    url(r"^faculty-pending/", views.faculty_remaining),
    url(r"^dashboard/", views.Dashboard, name="dashboard"),
    url(r"^notify/", views.notifyView, name="notify"),
    url(r"^completed/", views.counter_view, name="counter_view"),
    url(r"^send_message/", views.send_text_message_view, name="send_text_message_view"),
    url(r"^progress/", views.show_message_sent_view, name="show_message_sent_view"),
    url(r"^ping-report/$", views.ping_url, name="ping_url"),
    url(r"^test-mode", views.test_mode, name="test_mode"),
    url(r"^institute-start", views.start_institute_feedback, name="institute_start"),
    # Easy Upload URLs
    url(r"^easy-upload/home", views.easy_upload, name="easy_upload"),
    url(r"^easy-upload/subject", views.easy_upload_subject, name="easy_upload_subject"),
    url(r"^easy-upload/teaches", views.easy_upload_teaches, name="easy_upload_teaches"),
    url(r"^easy-upload/users", views.easy_upload_users, name="easy_upload_users"),
    url(r"^easy-upload/summary", views.easy_upload_test, name="easy_upload_test"),
    url(r"^easy-upload/message", views.easy_upload_message, name="easy_upload_message"),
    url(r"^easy-upload/settings", views.easy_upload_settings, name="easy_upload_settings"),
    url(r"^easy-upload/teacher-list", views.teachers_list, name="easy_upload_teacher_list"),
    # url(r'^consolidated/', views.consolidated.as_view(), name='feedback/consolidated_report'),
]
