from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import *

from import_export.admin import ImportExportModelAdmin
from import_export import resources

admin.site.site_header = "BMSIT Feedback System Admin Interface"


class UserResource(resources.ModelResource):
	class Meta:
		model = User


class TeachesResource(resources.ModelResource):
	class Meta:
		model = Teaches


class SubjectResource(resources.ModelResource):
	class Meta:
		model = Subject

class OTPTrackResource(resources.ModelResource):
	class Meta:
		model = OTPTrack

@admin.register(User)
class UserAdmin(DjangoUserAdmin, ImportExportModelAdmin):

	add_fieldsets = (
		(None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
	)

	list_display = ("username", "first_name", "electives", "phone", "sem", "sec")
	search_fields = ("email", "first_name", "last_name", "username", "phone")
	ordering = ("username",)

	list_filter = ('sem', 'sec', 'department', 'elective', 'batch', 'sub_batch')

	resource_class = UserResource

	def save_model(self, request, obj, form, change):
		if getattr(obj, 'user', None) is None:
			obj.user = request.user
		obj.save()

	def get_queryset(self, request):
		qs = super(UserAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(department=request.user.department)

	def electives(self, obj):
		return ", ".join([p.name for p in obj.elective.all()])

	def get_fieldsets(self, request, obj=None):
		if not request.user.is_superuser:
			return (
				(None, {"fields": ("username", "email", "password")}),
				(
					("Personal info"),
					{
						"fields": (
							"first_name",
							"last_name",
							"phone",
							"date_of_joining",
						)
					},
				),
				(
					("Permissions"),
					{
						"fields": (
							"is_active",
							"is_staff",
							"is_superuser",
							"groups",
							"user_permissions",
						)
					},
				),
				(
					("Academic Details"),
					{"fields": ("sem", "sec", "elective", "batch", "sub_batch")},
				),
				(("Designation"), {"fields": ("user_type", "ug")}),
				(("Important dates"), {"fields": ("last_login", "date_joined")}),
				(("Completion"), {"fields": ("institute", "done")}),
			)
		return (
			(None, {"fields": ("username", "email", "password")}),
			(
				("Personal info"),
				{
					"fields": (
						"first_name",
						"last_name",
						"phone",
						"date_of_joining",
						"department",
					)
				},
			),
			(
				("Permissions"),
				{
					"fields": (
						"is_active",
						"is_staff",
						"is_superuser",
						"groups",
						"user_permissions",
					)
				},
			),
			(
				("Academic Details"),
				{"fields": ("sem", "sec", "elective", "batch", "sub_batch")},
			),
			(("Designation"), {"fields": ("user_type", "ug")}),
			(("Important dates"), {"fields": ("last_login", "date_joined")}),
			(("Completion"), {"fields": ("institute", "done")}),
		)


@admin.register(Teaches)
class TeachesAdmin(ImportExportModelAdmin):
	list_display = (
		"teachers_first_name",
		"subject_name",
		"semester",
		"sec",
		"department_name",
		"batch",
		"sub_batch",
		"ug",
	)
	search_fields = ("teacher__first_name", "subject__name", "subject__code")
	list_filter = ('sec', 'sem', 'department')

	resource_class = TeachesResource

	def save_model(self, request, obj, form, change):
		if getattr(obj, 'user', None) is None:
			obj.user = request.user
		obj.save()

	def get_queryset(self, request):
		qs = super(TeachesAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(department=request.user.department)

	def teachers_first_name(self, instance):
		return instance.teacher.first_name

	def subject_name(self, instance):
		return instance.subject.name

	def department_name(self, instance):
		return instance.department.name

	def semester(self, instance):
		return instance.sem.sem


@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
	list_display = ("name", "code", "theory", "elective", "project")
	search_fields = ("name", "code")
	resource_class = SubjectResource

@admin.register(OTPTrack)
class SubjectAdmin(ImportExportModelAdmin):
	list_display = ("usn", "date_stamp", "time_stamp")
	search_fields = ("usn",)
	resource_class = OTPTrackResource


admin.site.register(Department)
admin.site.register(Semester)
admin.site.register(UserType)
admin.site.register(Message)

