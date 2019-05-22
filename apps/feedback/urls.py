from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
	# url(r'^report/', TemplateView.as_view(template_name='report_closed_for_feedback.html'), name='report'),
	# url(r'^reportstudent/(?P<username>[-\w]+)/$',TemplateView.as_view(template_name='report_closed_for_feedback.html'), name='reportstudent'),
	# url(r'^sreports/(?P<username>[-\w.]+)/$',TemplateView.as_view(template_name='report_closed_for_feedback.html'), name='sconsolidated'),
	# url(r'^report-select-hod/$',TemplateView.as_view(template_name='report_closed_for_feedback.html'), name='hod-select-faculty'),
	# url(r'^consolidated/$',TemplateView.as_view(template_name='report_closed_for_feedback.html'), name='consolidated'),
	# url(r'^consolidated_sixty/$',TemplateView.as_view(template_name='report_closed_for_feedback.html'), name='consolidated_sixty'),
	# url(r'^report-principal/$',TemplateView.as_view(template_name='report_closed_for_feedback.html'), name='principal-select-faculty'),
	url(r"^entry/", views.FeedbackView.as_view(), name="feedback_form"),
	# If report portal is to be CLOSED, comment below, else comment above
	url(r"^report/", views.Report.as_view(), name="report"),
	url(r'^__/__/--/__/__reports/(?P<username>[-\w]+)/$',views.consolidated, name='reports-url'),
	url(r"^reportstudent/(?P<username>[-\w]+)/$",views.Student_Report.as_view(),name="reportstudent"),
	url(r"^sreports/(?P<username>[-\w.]+)/$", views.sconsolidated, name="sconsolidated"),
	url(r"^report-select-hod/$",views.select_teacher_hod.as_view(),name="hod-select-faculty"),
	url(r"^consolidated/$", views.view_consolidated, name="consolidated"),
	url(r"^student-consolidated/$", views.student_view_consolidated, name="student_consolidated"),
	url(r"^student-consolidated-sixty/$",views.student_view_consolidated_sixty,name="consolidated_sixty"),
	url(r"^report-principal/$",views.select_teacher_principal.as_view(),name="principal-select-faculty"),
	url(r"^select-report/$",views.select_report.as_view(),name="select_report"),
	url(r"^previous-report/(?P<id>[-\w.]+)/$",views.previous_consolidated,name="previous_reports"),

	url(r"^select-p2p-report/$",views.select_p2p_report.as_view(),name="select_p2p_report"),
	url(r"^previous-p2p-report/(?P<id>[-\w.]+)/$",views.previous_p2p_consolidated,name="previous_p2p_reports"),

	url(r"^teacher-select-report/$",views.teacher_select_report.as_view(),name="teacher_select_report"),
	url(r"^teacher-previous-report/(?P<id>[-\w.]+)/$",views.teacher_previous_reports,name="teacher_previous_reports"),

	url(r"^teacher-select-p2p-report/$",views.teacher_select_p2p_report.as_view(),name="teacher_select_p2p_report"),
	url(r"^teacher-previous-p2p-report/(?P<id>[-\w.]+)/$",views.teacher_previous_p2p_reports,name="teacher_previous_p2p_reports"),

	url(r"^__/__/--/__/__sreports/(?P<username>[-\w.]+)/$",views.Test_report,name="sreports-url"),
]

