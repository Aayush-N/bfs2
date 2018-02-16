from django.db import models
from django.contrib.auth.models import AbstractUser, User

class Department(models.Model):
	'''
	Department: Holds the name of the department
	'''
	name = models.CharField("Name", max_length=250, help_text='Name of the department')

	def __str__(self):
		return self.name

class User(AbstractUser):
	'''
	User: Holds details about the user. By default the user is a Student. 
	The user's designation will be checked in the below checkboxes.
	If the user is a HOD and also teaches, both faculty and HOD will be True.
	We are considering the Institution as a user.
	'''
	phone = models.CharField("Phone", max_length=15, null=True, blank=True)
	sem = models.IntegerField("Semester", null=True, blank=True)
	sec = models.CharField("Section", max_length=10, null=True, blank=True)
	department = models.ForeignKey("Department", on_delete=models.CASCADE, null=True)
	date_of_joining = models.DateField("Date of Joining", null=True, blank=True)

	elective = models.ManyToManyField("subject", null=True, blank=True)
	batch = models.CharField("Lab Batch", max_length=50, null=True, blank=True)
	sub_batch = models.CharField("Lab Sub Batch", max_length=50, null=True, blank=True)

	# Below Boolean Fields denote the designation of the user
	faculty = models.BooleanField(default=False)
	hod = models.BooleanField(default=False)
	vice_principal = models.BooleanField(default=False) 
	principal = models.BooleanField(default=False)
	institution = models.BooleanField(default=False)

	# If a user abonds the feedback, partially done becomes true then 
	# the user is restricted from giving feedback.
	partially_done = models.BooleanField(default=False)
	done = models.BooleanField(default=False)


class Subject(models.Model):
	'''
	Subject: Holds details about each subject
	'''
	name = models.CharField("Subject Name", max_length=50)
	code = models.CharField("Subject Code", max_length=50)

	theory = models.BooleanField(default=True)
	elective = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class Teaches(models.Model):
	'''
	Teaches: Holds details about the subject that the teacher teaches.
	It links the Subject and the Teacher with the sem, sec and department that they are teaching.
	We are storing sem, sec, deaprtment of the student to get the name of the teacher by matching the 
	details with the user table.

	Note: Even if one student studies an elective in another department under the other department teacher,
	a new row has to be added.
	'''
	teacher = models.ForeignKey('user')
	subject = models.ForeignKey('subject')

	sem = models.CharField("Student's Semester", max_length=50)
	sec = models.CharField("Student's Section", max_length=50)
	department = models.ForeignKey('department', verbose_name="Student's department")

	batch = models.CharField("Student's Batch", max_length=50, null=True, blank=True)
	sub_batch = models.CharField("Student's sub batch", max_length=50, null=True, blank=True)

	def __str__(self):
		return self.teacher.first_name + ' -> '  + self.subject.name



