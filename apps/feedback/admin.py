from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import *

admin.site.register(ConsolidatedReport)
admin.site.register(FeedbackProcess)


class StudentConsolidatedResource(resources.ModelResource):
    class Meta:
        model = StudentConsolidatedReport

class FeedbackFormResource(resources.ModelResource):
    class Meta:
        model = FeedbackForm

class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):

    fieldsets = ((None, {"fields": ("question", "teacher", "form", "recipient")}),)


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):

    fieldsets = ((None, {"fields": ("question", "teacher", "form", "recipient")}),)
    search_fields = ("teacher__teacher__first_name",)
    list_display = ["teacher", "get_code"]

    def get_code(self, obj):
        return obj.form.code


@admin.register(StudentConsolidatedReport)
class StudentConsolidatedAdmin(ImportExportModelAdmin):
    resource_class = StudentConsolidatedResource

    def __str__(self):
    	return self.name + self.count

@admin.register(FeedbackForm)
class FeedbackFormAdmin(ImportExportModelAdmin):
    resource_class = FeedbackFormResource


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource