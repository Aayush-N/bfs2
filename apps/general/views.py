"""
Copyright 2017 DevX Labs
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
	http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.core import serializers
from django.forms.models import model_to_dict
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

import json
import csv
import pandas as pd
import numpy
import math
import string

from django.views import View
from django.views.generic import TemplateView, FormView
from django.core.urlresolvers import resolve
from django.contrib.auth import logout

from .models import User
from apps.feedback.models import *

from apps.feedback.forms import FeedbackAnswerForm, FeedbackProcessForm

from django.contrib.auth.hashers import make_password, check_password
import random
import urllib.parse as ap
import urllib.request
from django.core.mail import send_mail, EmailMessage

from .models import *
from .forms import *
from django.db.models import Avg


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from smtplib import SMTP_SSL as SMTP


# Send email, text message
import psycopg2

import urllib.parse as ap
import urllib.request

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

def page_not_found_view(request):
	template_name = "404.html"
	context = {}
	return render(request, template_name, context)


def internal_server_error_view(request):
	error_url = request.get_full_path()
	template_name = "500.html"
	context = {"error_url": error_url}
	return render(request, template_name, context)


def notifyView(request):
	"""
	notifyView: Notifies the Administrators if there are any errors
	occured in the website.
	"""
	error_url = request.GET.get("q", "directly reached notify")
	print(error_url)
	template_name = "notify.html"
	context = {}
	email = EmailMessage(
		"Feedback Error occurred at " + str(error_url),
		'Hi Administrator,\nThere is a 500 error reported at "'
		+ str(error_url)
		+ '".\nThis request was made by: '
		+ str(request.user)
		+ "\nPlease look into it immediately.\n\nThanks,\nBFS-BMSIT",
		"Feedback Support <feedback@bmsit.in>",
		["nandkeolyar.aayush@gmail.com", "amoghsk279@gmail.com", "kumarvinay937@gmail.com", "adarshkumar.sah6@gmail.com"],
	)
	email.send()
	return render(request, template_name, context)


class HomeView(FormView):
	"""
	Generates OTP, checks if user exists and has an email address.
	"""

	template_name = "index.html"

	def phone_otp(self, random_otp, phone, usn):
		"""
		Sends OTP to phone
		"""
		phone1 = phone
		message = "Please login with the OTP: " + random_otp + " for USN:" + usn
		params = {"number": phone1, "text": message}
		baseUrl = (
			"https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey=62sxGWT6MkCjDul6eNKejw&senderid=BMSITM&channel=2&DCS=0&flashsms=0&"
			+ ap.urlencode(params)
		)
		#urllib.request.urlopen(baseUrl).read(1000)
		OTPTrack.objects.create(phone=phone, usn=usn)

	def password_update(self, random_otp, usn):
		"""
		Hashes the new password according to the OTP
		"""
		hashed_pwd = make_password(random_otp)
		User.objects.filter(username=usn).update(password=hashed_pwd)

	def email_otp(self, random_otp, qs):
		"""
		Sends OTP to email
		"""

		body = "Hi, "\
			+ qs.first_name\
			+ "\n\n"\
			+ "Your OTP for feedback is: "\
			+ random_otp\
			+ "\n\nThanks,\nBFS-BMSIT"

		if qs.department.name == 'CSE':
			fromaddr = "feedbackcseotp@bmsit.in"
		elif qs.department.name == 'ECE':
			fromaddr = "feedbackeceotp@bmsit.in"
		elif qs.department.name == 'ISE':
			fromaddr = "feedbackiseotp@bmsit.in"
		elif qs.department.name == 'CIVIL':
			fromaddr = "feedbackcseotp@bmsit.in"
		elif qs.department.name == 'EEE':
			fromaddr = "feedbackeeeotp@bmsit.in"
		elif qs.department.name == 'MECH':
			fromaddr = "feedbackmechotp@bmsit.in"
		elif qs.department.name == 'TCE':
			fromaddr = "feedbacktceotp@bmsit.in"
		elif qs.department.name == 'MCA':
			fromaddr = "feedbackeceotp@bmsit.in"
		else:
			email = EmailMessage(
				"Feedback OTP",
				"Hi, "
				+ qs.first_name
				+ "\n\n"
				+ "Your OTP for feedback is: "
				+ random_otp
				+ "\n\nThanks,\nBFS-BMSIT",
				"Feedback Support <feedback@bmsit.ac.in>",
				[qs.email],
			)
			#email.send()
			OTPTrack.objects.create(email=qs.email, usn=qs.username)
			return

		msg = MIMEText(body, 'plain')
		msg['To'] = qs.email
		msg['Subject'] = "Feedback OTP"

		server = SMTP('smtp.gmail.com')
		server.login(fromaddr, "Feedback@01")
		server.sendmail(fromaddr, qs.email, msg.as_string())
		server.quit()

	def feedback_over_view(self, request):
		template_name = "feedback_over_final.html"
		return render(request, template_name)

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

	def post(self, request, *args, **kwargs):
		random_otp = r"".join(random.choice("0123456789") for i in range(4))
		try:
			otp_page = "login.html"
			usn = request.POST.get("usn1")
			usn = usn.upper()
			otp_page = otp_page + "/usn/" + usn
			qs = get_user_model().objects.get(username=usn)

			# Checks if user is admin and redirects directly
			if qs.is_superuser:
				messages.error(request, "Remember Admin, with great power comes great responsibility.")
				return HttpResponseRedirect("/login/usn=" + usn)

				# Checks if done=False
			if not qs.done or not qs.is_student():

				if qs:
					# Checks if both email and phone doesn't exist
					if qs.department.test_mode:
						self.password_update(random_otp, usn)
						messages.error(
							request, "The OTP is \n" + random_otp + "NOTE: If you're a student please don't give feedback, your answers won't be saved. Please contact your department coordinator."
							)
						return HttpResponseRedirect("/login/usn=" + usn)

					elif not qs.email and not qs.phone:
						messages.error(
							request, "Contact details incomplete. Contact coordinator"
						)

					# Checks if both email and phone exist
					elif qs.email and qs.phone:
						self.phone_otp(random_otp, qs.phone, qs.username)
						self.email_otp(random_otp, qs)
						self.password_update(random_otp, usn)
						# print("OTP: ", random_otp)
						messages.error(
							request, "OTP sent to " + qs.phone + " and " + qs.email
							# request, "The OTP is \n" + random_otp
						)
						return HttpResponseRedirect("/login/usn=" + usn)

						# Checks if only phone exists
					elif qs.phone and not qs.email:
						self.phone_otp(random_otp, qs.phone, usn)
						self.password_update(random_otp, usn)
						messages.error(
							request, "Email not found, OTP sent to " + qs.phone
						)
						return HttpResponseRedirect("/login/usn=" + usn)

						# Checks if only email exists
					elif qs.email and not qs.phone:
						self.email_otp(random_otp, qs)
						self.password_update(random_otp, usn)
						messages.error(
							request, "Phone number not found, OTP  sent to " + qs.email
						)
						return HttpResponseRedirect("/login/usn=" + usn)

			else:
				messages.error(
					request, "You have already given the feedback! Thank You."
				)

		except User.DoesNotExist:
			messages.error(request, "Invalid USN")
		return render(request, self.template_name)


def done_view(request):
	"""
	Gets the rating after completion of feedback and redirects to home page.
	"""
	# rating = request.GET.get("rating")
	# if str(rating) == 'None':
	# 	rating = 5
	# starts = Rating.objects.create(star=rating)
	return redirect("/")


def exit_view(request):
	"""
	Displays the rating page
	"""
	logout(request)
	template_name = "exit.html"
	return render(request, template_name)


def get_rating_view(request):
	"""
	Displays the current average rating
	"""
	template_name = "rating.html"
	rating = Rating.objects.aggregate(Avg("star"))
	rating = rating["star__avg"]
	context = {"rating": rating}
	return render(request, template_name, context)


class MainView(TemplateView):
	"""
	Checks for the type of user and renders the count and users of their mandatory
	forms.
	All the other individual forms are generated subsequently

	Passing the following to the variabes to the session
	`faclties` - if the user is a faculty, a list of all the faculties of
		same department except the the user is stored
	`hods` - if the user is hod, a list all the hods from different departments
		 are stored
	`count` - it is the total no of forms that the user needs to give feedback for.
		ie, for a faculty no. of collegues + no of individual forms

	TODO://
		1 - Move this to general `views.py` . Doesn't belong here
		2 - Add student check
	"""

	template_name = ""
	user_type = None

	def _student_theory(self):
		subject_list = []
		theory_subject = Teaches.objects.filter(
			sem=self.user.sem,
			sec=self.user.sec,
			department=self.user.department,
			subject__theory=True,
			subject__elective=False,
			subject__project=False,
			ug=self.user.ug,
			is_active=True,
		)
		for i in theory_subject:
			subject_list.append(i.pk)

		elective_subject = Teaches.objects.filter(
			sem=self.user.sem,
			sec=self.user.sec,
			department=self.user.department,
			subject__theory=True,
			subject__elective=True,
			ug=self.user.ug,
			subject__in=self.user.elective.all(),
			is_active=True,
		)
		for i in elective_subject:
			subject_list.append(i.pk)

		self.request.session["recipients_theory"] = subject_list

		# This is used in post and will be removed on by one
		self.request.session["post_recipients_theory"] = subject_list

		self.request.session["theory_count"] = (
			theory_subject.count() + elective_subject.count()
		)

		# remove the form as it is already counted
		self.forms = self.forms.exclude(code="ST")

		return

	def _student_labs(self):

		subject_list = []
		lab_subject = Teaches.objects.filter(
			sem=self.user.sem,
			sec=self.user.sec,
			department=self.user.department,
			subject__theory=False,
			subject__project=False,
			sub_batch=self.user.sub_batch,
			batch=self.user.batch,
			ug=self.user.ug,
		)
		for i in lab_subject:
			subject_list.append(i.pk)

		self.request.session["recipients_labs"] = subject_list

		# This is used in post and will be removed on by one
		self.request.session["post_recipients_labs"] = subject_list

		self.request.session["labs_count"] = lab_subject.count()

		# remove the form as it is already counted
		self.forms = self.forms.exclude(code="SL")

		return

	def _student_project(self):

		subject_list = []
		project_subject = Teaches.objects.filter(
			sem=self.user.sem,
			sec=self.user.sec,
			batch=self.user.batch,
			department=self.user.department,
			subject__project=True,
			subject__theory=False,
			subject__elective=False,
			ug=self.user.ug,
			is_active=True,
		)
		for i in project_subject:
			subject_list.append(i.pk)

		self.request.session["recipients_project"] = subject_list

		# This is used in post and will be removed on by one
		self.request.session["post_recipients_project"] = subject_list

		self.request.session["project_count"] = project_subject.count()

		# remove the form as it is already counted
		self.forms = self.forms.exclude(code="SP")

		return

	def _faculty_mandatory(self):
		"""
		This is a compulsory form for the faculty where they give the
		feedack to he other faculties
		"""

		# if the hod is also a faculty, he should be removed form the `faculties` list
		hod = UserType.objects.get(name="Hod")

		faculties = (
			get_user_model()
			.objects.filter(
				department=self.user.department, user_type__in=self.user_types
			)
			.exclude(pk=self.user.pk)
		)

		recipient_list = []
		for i in faculties:
			recipient_list.append(i.pk)
		self.request.session["recipients"] = recipient_list

		# This is used in post and will be removed on by one
		self.request.session["post_recipients"] = recipient_list

		self.request.session["count"] = faculties.count()

		# remove the form as it is already counted
		self.forms = self.forms.exclude(code="FF")

		return

	def _hod_mandatory(self):
		"""
		Compulsory form for HOD where they give feedback to the department HODs
		"""
		faculty = UserType.objects.get(name="Faculty")
		hods = (
			get_user_model()
			.objects.filter(user_type__in=self.user_types)
			.exclude(pk=self.user.pk)
		)
		recipient_list = []
		for i in hods:
			recipient_list.append(i.pk)
		self.request.session["recipients"] = recipient_list

		# This is used in post and will be removed on by one
		self.request.session["post_recipients"] = recipient_list

		self.request.session["count"] = hods.count()
		# remove the form as it is already counted
		self.forms = self.forms.exclude(code="HH")

		return

	def get_context_data(self, **kwargs):
		context = super(MainView, self).get_context_data(**kwargs)
		self.user = self.request.user
		self.user_types = self.user.user_type.all()
		self.request.session["count"] = 0

		if self.user.is_student():
			self.forms = FeedbackForm.objects.filter(
				active=True, user_type__in=self.user_types
			)
			self._student_theory()
			self._student_labs()
			self._student_project()
			# if the user is hod as well as faculty, faculties mandatory forms shouldn't
			# be displayed
		elif self.user.is_faculty() and not self.user.is_hod():
			self.forms = FeedbackForm.objects.filter(
				active=True, user_type__in=self.user_types
			)
			self._faculty_mandatory()

		elif self.user.is_hod():
			# faculty mandatory forms are not required, so removed them
			faculty = UserType.objects.get(name="Faculty")

			self.user_types = self.user_types.exclude(name="Faculty")
			self.forms = FeedbackForm.objects.filter(
				active=True, user_type__in=self.user_types
			)

			self._hod_mandatory()

		else:
			self.forms = FeedbackForm.objects.filter(
				active=True, user_type__in=self.user_types
			)

		accounts = Department.objects.get(pk=16)
		if self.user.department == accounts:
			self.forms = self.forms.exclude(code="OH")

		if self.request.user.is_student():
			self.request.session["count"] = (
				self.request.session["theory_count"]
				+ self.request.session["labs_count"]
				+ self.request.session["project_count"]
			)

		for form in self.forms:
			self.request.session["count"] += 1

		form_list = list()
		for f in self.forms:
			form_list.append(f.pk)
		self.request.session["form"] = form_list

		# they are the remaining recipients of the iterable forms
		form_recipients = list()
		for f in self.forms:
			form_recipients.append(f.recipient.name)

		self.request.session["form_recipients"] = form_recipients

		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)

		if self.user.is_superuser:
			return HttpResponseRedirect(reverse_lazy("dashboard"))

		if not self.user.is_student() and self.user.done:
			return HttpResponseRedirect(reverse_lazy("dashboard"))

		return HttpResponseRedirect("/entry")

	def serialize_obj(self, obj):
		data = serializers.serialize("json", obj)
		struct = json.loads(data)
		data = json.dumps(struct[0])
		return data


def faculty_remaining(request):
	"""
	faculty_remaining: Sends email with the list of people who
	haven't submitted the feedback.
	"""
	conn = psycopg2.connect(
		database="feedback",
		user="postgres",
		password="feedback321",
		host="128.199.250.218",
		port="5433",
	)
	cursor = conn.cursor()

	cursor.execute(
		"SELECT department_id, first_name  FROM general_user WHERE done = 'false' GROUP BY department_id, first_name ORDER BY department_id, first_name "
	)
	data = cursor.fetchall()
	count = len(data) - 4
	str1 = "Pending: %d/194\nDepartment Name\n" % (count)
	data = data[:-4]

	for i in data:
		str1 += "%s %s\n" % (i[0], i[1].title())

	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login("feedback@bmsit.in", "Feedback@01")

	fromaddr = "feedback@bmsit.in"
	toaddr = "vishakhay@bmsit.in"
	msg = MIMEMultipart()
	msg["From"] = fromaddr
	msg["To"] = toaddr.strip()
	msg["Subject"] = "Feedback pending"
	body = str1
	msg.attach(MIMEText(body, "plain"))
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	template_name = "faculty_pending.html"
	return render(request, template_name)


def counter_view(request):
	"""
	Displays the total number of students who have given feedback
	"""
	total_done = 0
	student_count = 0
	count = User.objects.all().filter(is_active=True)
	for i in count:
		if i.is_student():
			student_count += 1
			if i.done == True:
				total_done += 1
	template_name = "counter.html"
	context = {"total": total_done, "student_count": student_count}
	return render(request, template_name, context)


def send_text_message_view(request):
	"""
	This view is used to send the message.
	"""
	students = User.objects.filter(
		user_type__name="Student", done=False, is_superuser=False, username='1BY15CS008'
	)
	total = len(students)
	message = Message.objects.first()
	context = {"total": total - 1, "message": message}
	return render(request, "send_message.html", context)


import time


def show_message_sent_view(request):
	"""
	This view actually sends the message.
	"""

	def generate():
		students = User.objects.filter(user_type__name="Student", done=False, username='1BY15CS008')
		c = 0
		message = Message.objects.first()
		for n, i in enumerate(students):
			yield "data:" + str(n) + "\n\n"
			text_message = str(str(message) % (i.first_name, i.username))
			params = {"number": i.phone, "text": text_message}
			baseUrl = (
				"https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey=62sxGWT6MkCjDul6eNKejw&senderid=BMSITM&channel=2&DCS=0&flashsms=0&"
				+ ap.urlencode(params)
			)
			urllib.request.urlopen(baseUrl).read(1000)
			time.sleep(0.01)
			c += 1
			print("Message sent to %s [%s] - %s" % (i.first_name, i.phone, i.username))
			# x = 0

			# while x <= 100:
			# 	yield "data:" + str(x) + "\n\n"
			# 	x = x + 10
			# 	time.sleep(0.5)

	return StreamingHttpResponse(generate(), content_type="text/event-stream")
	# conn = psycopg2.connect(database='feedback', user='postgres', password='feedback321', host='128.199.250.218', port='5431')
	# cursor = conn.cursor()

	# cursor.execute("SELECT first_name, phone, username FROM general_user WHERE username = '%s';" %(i))
	# data = cursor.fetchall()

	# # for i in data:
	# #     if i[0] != 'HOD_SPORTS':
	# #         print(i[0], i[1], i[2], i[3])
	# `t = 0
	# message = ''

	# for i in data:
	#     # print(i[0],i[1],i[2],i[3], i[4])
	#     # \nYou are required to submit the second feedback using the URL: https://feedback360.bmsit.ac.in. Complete it ASAP. In case of inconvenience submit your query in the help form. The process ends by 1st of May 2018.
	#     message = 'Dear %s,\n\nYour Username: %s\n\nPowered by DevX' %(i[0],i[2])
	#     params = { 'number' : i[1], 'text' : message }
	#     baseUrl = 'https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey=62sxGWT6MkCjDul6eNKejw&senderid=BMSITM&channel=2&DCS=0&flashsms=0&' + ap.urlencode(params)
	#     urllib.request.urlopen(baseUrl).read(1000)
	#     print("Message sent to %s [%s]" %(i[0],i[1]))


import requests


def ping_url(request):
	"""
	This view is used to open reports of each and every faculty members.
	This is used to store the consolidated report data.
	"""
	
	data = User.objects.filter(user_type__name="Faculty")
	count = 0

	for teacher in data:
		try:
			r = requests.get(
				"https://feedback360.bmsit.ac.in/__/__/--/__/__sreports/%s/" % (teacher.username)
			)
			count += 1
		except:
			pass
	messages.success(request, 'All %d faculty reports generated.' %(count))

	# print("Count", count)

	return HttpResponseRedirect('/easy-upload/settings')


# @login_required(login_url='/signin/')
# def main_view(request):
# 	'''
# 	Takes the user's subjects, segragates them into theory, lab and elective
# 	Passes subject details and faculty details to feedback view
# 	'''
# 	user = request.user.profile

# 	# Taking total subject count - IF WORKS, TO BE REMOVED
# 	# total = Subject.objects.filter(semester=user.semester,
# 	#                     dno=user.dno).count()

# 	# Getting all the subjects instances
# 	if user.mtech:
# 		sub_obj = Subject.objects.filter(semester=user.semester,
# 						dno=user.dno, mtech=True)
# 	else:
# 		sub_obj = Subject.objects.filter(semester=user.semester,
# 						dno=user.dno, mtech=False)

# 	sub_list = []
# 	sub_list_name = []

# 	# Getting `sub_code` to get the `*teaches` model
# 	for i in sub_obj:
# 		sub_list.append(i.sub_code)

# 	faculty = []

# 	# Getting theory subjects
# 	for sub in sub_list:
# 		try:
# 			if user.mtech:
# 				f = TheoryTeaches.objects.get(sub_code=sub, section=user.section)
# 			else:
# 				f = TheoryTeaches.objects.get(sub_code=sub, section=user.section)
# 			faculty.append(f)
# 		except TheoryTeaches.DoesNotExist:
# 			pass

# 	# Semester from where elective subjects starts
# 	# This is essential, change if semester changes
# 	eletive_semester = 5

# 	# Max no of electives in a semester, should be chnaged if no chnages
# 	no_of_elective = 2

# 	# Fir m

# 	# Only accessed if student has electives
# 	if user.semester >= eletive_semester and not user.mtech and user.dno.dno is not 8:
# 		f = [] # Getting elecitves
# 		for sub in sub_list:
# 			try:
# 				f.append(ElectiveTeaches.objects.get(sub_code__sub_code=user.elective1_id, section=user.section))
# 				f.append(ElectiveTeaches.objects.get(sub_code__sub_code=user.elective2_id, section=user.section))

# 			except ElectiveTeaches.DoesNotExist:
# 				pass
# 		for i in range(0, no_of_elective):
# 			faculty.append(f[i])

# 	# this is for mca, should go in different function
# 	if user.dno.dno == 8 and user.semester == 3:
# 		f = []
# 		for sub in sub_list:

# 			try:
# 				f.append(ElectiveTeaches.objects.get(sub_code__sub_code=user.elective1_id, section=user.section))

# 			except ElectiveTeaches.DoesNotExist:
# 				pass
# 		for i in range(0, 1):
# 			faculty.append(f[i])

# 	# this is for mtech
# 	if user.mtech:
# 		f = []
# 		for sub in sub_list:

# 			try:
# 				f.append(ElectiveTeaches.objects.get(sub_code__sub_code=user.elective1_id, section=user.section))

# 			except ElectiveTeaches.DoesNotExist:
# 				pass
# 		for i in range(0, 1):
# 			faculty.append(f[i])

# 	# Getting lab subjects
# 	for sub in sub_list:
# 		# This is for 1st sem, lab_sub_code ka chutiyapa
# 		if user.semester == 1:
# 			f = LabTeaches.objects.filter(sub_code=sub, section=user.section,
# 				lab_batch=user.lab_batch, lab_sub_code=user.lab_sub_code)
# 		else:
# 			f = LabTeaches.objects.filter(sub_code=sub, section=user.section, lab_batch=user.lab_batch)
# 		for k in f:
# 			faculty.append(k)

# 	# getting faculty name from the subjects
# 	for i in faculty:
# 		sub_list_name.append(i.sub_code.sub_name)

# 	lab_count = 0
# 	theory_count = 0

# 	# Getting theory and lab count for the feedback page
# 	for fac in faculty:
# 		try :
# 			if fac.lab_batch:
# 				lab_count += 1
# 		except:
# 			theory_count += 1

# 	faculty_name = []
# 	faculty_id = []

# 	#getting faculty name
# 	for a in faculty:
# 		faculty_name.append(a.fid.fname)
# 	for a in faculty:
# 		faculty_id.append(a.fid.fid)

# 	sec = str(user.section)
# 	student_class = sec

# 	# should be added to context
# 	request.session['show_sub_list']    = sub_list_name
# 	sub_list_name.reverse()
# 	request.session['theory_count']     = theory_count
# 	request.session['lab_count']        = lab_count
# 	request.session['sub_code_list']    = sub_list_name
# 	request.session['name']             = request.user.first_name
# 	request.session['faculty']          = faculty_name
# 	request.session['faculty_id']       = faculty_id
# 	request.session['student_class']    = student_class

# 	user.login_done = 'True'
# 	user.save()
# 	return HttpResponseRedirect(reverse_lazy('feedback_entry'))


# def counter_view(request):
# 	'''
# 	Displays the total number of students who have given feedback
# 	'''
# 	total_done = 0
# 	count = UserProfile.objects.all()
# 	for i in count:
# 		if i.done == True:
# 			total_done += 1
# 	template_name = 'total.html'
# 	print(total_done)
# 	context = {"total" : total_done}
# 	return render(request, template_name, context)


def done_cron(request, dept_name):
	"""
	Downloads the list of remaing students, department wise in a CSV file
	"""
	student_list = User.objects.filter(
		department__name=dept_name, done=False, is_active=True
	).order_by("sem")
	response = HttpResponse(content_type="text/csv")

	response["Content-Disposition"] = (
		"attachment; filename=feedback_pending_" + dept_name + ".csv"
	)
	writer = csv.writer(response)
	for student in student_list:
		writer.writerow(
			[student.username, student.first_name, student.sem, student.sec]
		)
	writer.writerow(["Total Remaining", student_list.count()])

	return response


def Dashboard(request):
	"""
	Shows the dashboard values
	"""
	template_name = "dashboard.html"
	user = request.user
	user_type = user.get_user_type()
	superuser = user.is_superuser
	if user.groups.filter(name='feedback_admin').exists():
		feedback_admin = True
	else:
		feedback_admin = False
	total = (
		int(
			User.objects.filter(
				user_type__name="Student", department__name="CSE",is_active=True
			).count()
		)
		+ int(
			User.objects.filter(
				user_type__name="Student", department__name="ECE",is_active=True
			).count()
		)
		+ int(
			User.objects.filter(
				user_type__name="Student", department__name="MECH",is_active=True
			).count()
		)
		+ int(
			User.objects.filter(
				user_type__name="Student", department__name="TCE",is_active=True
			).count()
		)
		+ int(
			User.objects.filter(
				user_type__name="Student", department__name="EEE",is_active=True
			).count()
		)
		+ int(
			User.objects.filter(
				user_type__name="Student", department__name="CIV",is_active=True
			).count()
		)
		+ int(
			User.objects.filter(
				user_type__name="Student", department__name="ISE",is_active=True
			).count()
		)
		+ int(
			User.objects.filter(
				user_type__name="Student", department__name="MCA",is_active=True
			).count()
		)
	)
	done = User.objects.filter(user_type__name="Student", done=True).count()
	total_p = User.objects.filter(user_type__name="Student").count()
	total_percent = int(done / total_p * 100)
	context = {
		"feedback_admin":feedback_admin,
		"user_type": user_type[0].name,
		"username": user.username,
		"name": user.first_name,
		"cse": User.objects.filter(
			done=False, user_type__name="Student", department__name="CSE",is_active=True
		).count(),
		"ece": User.objects.filter(
			done=False, user_type__name="Student", department__name="ECE",is_active=True
		).count(),
		"mech": User.objects.filter(
			done=False, user_type__name="Student", department__name="MECH",is_active=True
		).count(),
		"tce": User.objects.filter(
			done=False, user_type__name="Student", department__name="TCE",is_active=True
		).count(),
		"eee": User.objects.filter(
			done=False, user_type__name="Student", department__name="EEE",is_active=True
		).count(),
		"civil": User.objects.filter(
			done=False, user_type__name="Student", department__name="CIVIL",is_active=True
		).count(),
		"ise": User.objects.filter(
			done=False, user_type__name="Student", department__name="ISE",is_active=True
		).count(),
		"mca": User.objects.filter(
			done=False, user_type__name="Student", department__name="MCA",is_active=True
		).count(),
		"cse_total": User.objects.filter(
			user_type__name="Student", department__name="CSE",is_active=True
		).count(),
		"ece_total": User.objects.filter(
			user_type__name="Student", department__name="ECE",is_active=True
		).count(),
		"mech_total": User.objects.filter(
			user_type__name="Student", department__name="MECH",is_active=True
		).count(),
		"tce_total": User.objects.filter(
			user_type__name="Student", department__name="TCE",is_active=True
		).count(),
		"eee_total": User.objects.filter(
			user_type__name="Student", department__name="EEE",is_active=True
		).count(),
		"civil_total": User.objects.filter(
			user_type__name="Student", department__name="CIVIL",is_active=True
		).count(),
		"ise_total": User.objects.filter(
			user_type__name="Student", department__name="ISE",is_active=True
		).count(),
		"mca_total": User.objects.filter(
			user_type__name="Student", department__name="MCA",is_active=True
		).count(),
		"total": total,
		"percent": total_percent,
		"superuser": superuser,
	}
	return render(request, template_name, context)


# 	def get_context_data(self, **kwargs):
# 		context = super(Dashboard, self).get_context_data(**kwargs)
# 		total_done = 0
# 		count = UserProfile.objects.all()
# 		total_count = UserProfile.objects.all().count()
# 		total_done = UserProfile.objects.filter(done=True).count()
# 		total_remaining = total_count - total_done
# 		context = {"total" : total_done, "total_remaining": total_remaining}
# 		news = News.objects.all().order_by('-pk')
# 		news = news[:5]
# 		context['news'] = news
# 		rating = Rating.objects.aggregate(Avg('star'))
# 		rating = rating['star__avg']
# 		context["rating"] = rating

# 		context['cse'] = UserProfile.objects.filter(done=False, dno_id=1).count()
# 		context['ise'] = UserProfile.objects.filter(done=False, dno_id=2).count()
# 		context['civil'] = UserProfile.objects.filter(done=False, dno_id=3).count()
# 		context['ece'] = UserProfile.objects.filter(done=False, dno_id=4).count()
# 		context['eee'] = UserProfile.objects.filter(done=False, dno_id=5).count()
# 		context['tce'] = UserProfile.objects.filter(done=False, dno_id=6).count()
# 		context['mech'] = UserProfile.objects.filter(done=False, dno_id=7).count()
# 		context['mca'] = UserProfile.objects.filter(done=False, dno_id=8).count()

# 		return context


#############################
# Easy Upload Views go here #
#############################

@login_required
def easy_upload_subject(request):
	"""
	"""
	template_name = "easy_upload/subject.html"

	if request.method == 'POST':

		errors = []
		updated = []
		added = []
		headers = ["name","code","type"]
		types = ['T', 'E', 'P', 'L', 'EL']

		try:
			csv_data = pd.read_csv(request.FILES['file'])

			csv_data = csv_data.apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('utf-8').str.strip() if x.dtype == "object" else x)
			# print(csv_data)

			count = 0
			head = list(csv_data.columns.values)

			# Check if CSV contains Correct values
			if len(head) == 3:
				for i in range(len(headers)):
					if head[i].lower() != headers[i]:
						errors.append("'%s' is an invalid field or in wrong order, Please rectify." %(head[i]))
			else:
				errors.append("Invalid number of columns provided!")

			# Check if CSV contains any null values
			if csv_data.isnull().values.any():
				errors.append("Your CSV Contains null value(s) please rectify!")

			# Check Subject Type
			sub_type = csv_data["type"].unique()
			for i in sub_type:
				if i.upper() not in types:
					errors.append("'%s' is an invalid subject type, Options are T (Theory), E (Elective) or P (Project)" %(i))
			if not errors:
				for data in csv_data.values:
					try:
						sub = Subject.objects.get(code=data[1].upper().strip())
						print("get",sub)
						if data[2].upper() == 'T':
							sub.name=data[0].title()
							sub.theory=True
							sub.elective=False
							sub.project=False
							sub.save()
							updated.append(data)

						elif data[2].upper() == 'E':
							sub.name=data[0].title()
							sub.theory=True
							sub.elective=True
							sub.project=False
							sub.save()
							updated.append(data)

						elif data[2].upper() == 'P':
							sub.name=data[0].title()
							sub.theory=False
							sub.elective=False
							sub.project=True
							sub.save()
							updated.append(data)

						elif data[2].upper() == 'L':
							sub.name=data[0].title()
							sub.theory=False
							sub.elective=False
							sub.project=False
							sub.save()
							updated.append(data)

						elif data[2].upper() == 'EL':
							sub.name=data[0].title()
							sub.theory=False
							sub.elective=True
							sub.project=False
							sub.save()
							updated.append(data)

					except:
						if data[2].upper() == 'T':
							Subject.objects.create(code=data[1].upper(), name=data[0], theory=True, elective=False, project=False)
							added.append(data)
						elif data[2].upper() == 'E':
							Subject.objects.create(code=data[1].upper(), name=data[0], theory=True, elective=True, project=False)
							added.append(data)
						elif data[2].upper() == 'P':
							Subject.objects.create(code=data[1].upper(), name=data[0], theory=False, elective=False, project=True)
							added.append(data)
						elif data[2].upper() == 'L':
							Subject.objects.create(code=data[1].upper(), name=data[0], theory=False, elective=False, project=False)
							added.append(data)
						elif data[2].upper() == 'EL':
							Subject.objects.create(code=data[1].upper(), name=data[0], theory=False, elective=True, project=False)
							added.append(data)

		except Exception as e:
			print("Exception", e)
			errors.append(e)

		context = {
		"errors":errors,
		"updated":updated,
		"added":added,
		"subject":True,
		'form': FileUploadForm(),
		}
		# print(data)
	else:
		context = {
		'form': FileUploadForm(),
		}

	return render(request, template_name, context)
		

	

@login_required
def easy_upload_teaches(request):
	"""
	"""

	template_name = "easy_upload/teaches.html"

	if request.method == 'POST':

		errors = []
		updated = []
		added = []
		headers = ["teacher","subject","sem","sec","batch","sub_batch","ug","count","is_active"]
		ug_types = ['Y', 'N']

		try:
			csv_data = pd.read_csv(request.FILES['file'])
			csv_data = csv_data.apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('utf-8').str.strip() if x.dtype == "object" else x)

			count = 0
			head = list(csv_data.columns.values)

			# Check if all the Headers are there
			if len(head) == 9:
				for i in range(len(headers)):
					if head[i].lower() != headers[i]:
						errors.append("'%s' is an invalid field or in wrong order, Please rectify." %(head[i]))
			else:
				errors.append("Invalid number of columns provided!")


			# Check for null values
			frames = [csv_data.iloc[:,:4], csv_data.iloc[:,6:]]
			nullvalues = pd.concat(frames, axis=1, sort=False)
			if nullvalues.isnull().values.any():
				errors.append("Your CSV Contains null value(s) please rectify!")

			# Check if right Ug value is entered or not
			ug = csv_data["ug"].unique()

			for i in ug:
				if i.upper() not in ug_types:
					errors.append("'%s' is an invalid ug value, Options are Y (Yes) or N (No)" %(i))

			# Check if right Ug value is entered or not
			is_active = csv_data["is_active"].unique()

			for i in is_active:
				if i.upper() not in ug_types:
					errors.append("'%s' is an invalid is_active value, Options are Y (Yes) or N (No)" %(i))

			# Check if the teacher exists or not
			teachers = csv_data["teacher"].unique()

			for teacher in teachers:
				try:
					teach = User.objects.get(id=teacher)
				except:
					errors.append("'%s' user does not exist! Please add to continue" %(teacher))

			# Check if Subject Exists or not
			subjects = csv_data["subject"].unique()

			for subject in subjects:
				try:
					sub = Subject.objects.get(code=subject.upper())
				except:
					errors.append("'%s' subject does not exist! Please add to continue" %(subject))

			# Check if semester is Correct
			semester = csv_data["sem"].unique()

			for sem in semester:
				if not sem in range(0,9):
					errors.append("'%s' invalid semester" %(sem))

			# If all the errors are corrected then the data is saved
			if not errors:
				for data in csv_data.values:
					try:
						teacher = User.objects.get(id=data[0])
						sem = Semester.objects.get(sem=data[2])
						subject = Subject.objects.get(code=data[1].upper())
						if data[8] == 'Y':
							is_active = True
						else:
							is_active = False
						# Check if Batch is null
						batch = None
						is_null = False

						try:
							is_null = math.isnan(float(data[4]))
						except:
							is_null = False

						if not is_null:
							batch = data[4].upper()

						# Check if Sub Batch is null
						sub_batch = None
						try:
							is_null = math.isnan(float(data[5]))
						except:
							is_null = False
						if not is_null:
							sub_batch = data[5].upper()


						teaches = Teaches.objects.get(teacher=teacher, subject=subject, sem=sem, sec=data[3], batch=batch, sub_batch=sub_batch)
						if data[6].upper() == 'Y':
							teaches.ug=True
							teaches.count=data[7]
							teaches.is_active=is_active
							teaches.save()
							updated.append(data)

						elif data[6].upper() == 'N':
							teaches.ug=False
							teaches.count=data[7]
							teaches.is_active=is_active
							teaches.save()
							updated.append(data)

					except Exception as e:
						# errors.append(e)
						# Check if Batch is null
						batch = None
						try:
							is_null = math.isnan(float(data[4]))
						except:
							is_null = False

						if not is_null:
							batch = data[4].upper()
						# Check if Sub Batch is null
						sub_batch = None
						try:
							is_null = math.isnan(float(data[5]))
						except:
							is_null = False
						if not is_null:
							sub_batch = data[5].upper()

						teacher = User.objects.get(id=data[0])
						sem = Semester.objects.get(sem=data[2])
						subject = Subject.objects.get(code=data[1].upper())
						if data[6].upper() == 'Y':
							Teaches.objects.create(teacher=teacher, subject=subject, sem=sem, sec=data[3], batch=batch, sub_batch=sub_batch, ug=True, count=data[7], department=request.user.department, is_active=is_active)
							added.append(data)
						elif data[6].upper() == 'N':
							Teaches.objects.create(teacher=teacher, subject=subject, sem=sem, sec=data[3], batch=batch, sub_batch=sub_batch, ug=False, count=data[7], department=request.user.department, is_active=is_active)
							added.append(data)

		except Exception as e:
			errors.append(e)

		context = {
		"errors":errors,
		"updated":updated,
		"added":added,
		"teaches":True,
		'form': FileUploadForm(),
		}
		# print(data)
	else:
		context = {
		'form': FileUploadForm(),
		}
	return render(request, template_name, context)

@login_required
def easy_upload_users(request):
	"""
	"""

	template_name = "easy_upload/users.html"

	if request.method == 'POST':

		errors = []
		updated = []
		added = []
		headers = ["username","first_name","email","is_active","phone","sem","sec","ug","batch","sub_batch","elective_1","elective_2","done"]
		bool_types = ['Y', 'N']

		try:
			csv_data = pd.read_csv(request.FILES['file'])
			csv_data = csv_data.apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('utf-8').str.strip() if x.dtype == "object" else x)

			# print(csv_data)
			# print(csv_data)

			count = 0
			head = list(csv_data.columns.values)

			# Check if all the Headers are there
			if len(head) == 13:
				for i in range(len(headers)):
					if head[i].lower() != headers[i]:
						errors.append("'%s' is an invalid field or in wrong order, Please rectify." %(head[i]))
			else:
				errors.append("Invalid number of columns provided!")


			# Check for null values
			frames = [csv_data.iloc[:,:2], csv_data.iloc[:,3:4], csv_data.iloc[:,5:8], csv_data.iloc[:,12:13]]
			nullvalues = pd.concat(frames, axis=1, sort=False)
			# print(nullvalues)
			if nullvalues.isnull().values.any():
				errors.append("Your CSV Contains null value(s) please rectify!")

			# Check if right Ug value is entered or not
			ug = csv_data["ug"].unique()

			for i in ug:
				if i.upper() not in bool_types:
					errors.append("'%s' is an invalid ug value, Options are Y (Yes) or N (No)" %(i))

			# Check if right is_active value is entered or not
			is_active = csv_data["is_active"].unique()

			for i in is_active:
				if i.upper() not in bool_types:
					errors.append("'%s' is an invalid is_active value, Options are Y (Yes) or N (No)" %(i))

			# Check if right done value is entered or not
			done = csv_data["done"].unique()

			for i in done:
				if i.upper() not in bool_types:
					errors.append("'%s' is an invalid is_active value, Options are Y (Yes) or N (No)" %(i))

			# Check if the Subjects exists or not
			subjects = numpy.concatenate((csv_data["elective_1"].unique(), csv_data["elective_2"].unique()))

			for subject in subjects:
				is_null = False
				try:
					is_null = math.isnan(float(subject))
				except:
					is_null = False

				if not is_null:
					try:
						sub = Subject.objects.get(code=subject.strip())
					except:
						errors.append("'%s' Subject does not exist! Please add to continue" %(subject))

			# Check if semester is Correct
			semester = csv_data["sem"].unique()

			for sem in semester:
				if not sem in range(0,9):
					errors.append("'%s' invalid semester" %(sem))

			# If all the errors are corrected then the data is saved
			if not errors:
				for data in csv_data.values:
					try:
						password = make_password(id_generator(8, "6793YUIO"))
						username = data[0].strip().upper()
						first_name = data[1].title()
						try:
							email = data[2].lower()
						except:
							email = data[2]
						is_active = False
						if data[3].upper() == 'Y':
							is_active = True
						phone = data[4]

						sem = Semester.objects.get(sem=data[5])

						sec = data[6].upper()
						department = request.user.department
						ug = False
						if data[7].upper() == 'Y':
							ug = True
						user_type = UserType.objects.get(name="Student")

						# Check if Batch is null
						batch = None
						is_null = False

						try:
							is_null = math.isnan(float(data[8]))
						except:
							is_null = False

						if not is_null:
							batch = data[8].upper()

						# Check if Sub Batch is null
						sub_batch = None
						try:
							is_null = math.isnan(float(data[9]))
						except:
							is_null = False
						if not is_null:
							sub_batch = data[9].upper()

						# Check if elecitves exists

						elective_1 = None
						is_null = False

						try:
							is_null = math.isnan(float(data[10]))
						except:
							is_null = False

						if not is_null:
							elective_1 = data[10].upper()

						elective_2 = None
						is_null = False

						try:
							is_null = math.isnan(float(data[11]))
						except:
							is_null = False

						if not is_null:
							elective_2 = data[11].upper()

						if data[12].upper() == 'Y':
							done = True
						else:
							done = False

						# print("Entered 1")
						user = User.objects.get(username=username)
						print(user.first_name)
						# print("Entered 2") 
						user.password=password
						user.first_name=first_name
						user.email = email
						user.is_active = is_active
						user.phone = phone
						user.sem = str(sem)
						user.sec = sec
						user.department = department
						user.ug = ug
						user.user_type.add(user_type)
						user.batch = batch
						user.sub_batch = sub_batch
						user.done = done
						

						# Check for number of elective
						electives = []


						if elective_1:
							electives.append(Subject.objects.get(code=elective_1))
						if elective_2:
							electives.append(Subject.objects.get(code=elective_2))

						# print("2--------------")
						user.elective.add(*electives)
						# print("3--------------")
						user.save()
						updated.append(data)

					except Exception as e:
						# errors.append(e)
						# Check if Batch is null
						password = make_password(id_generator(8, "6793YUIO"))
						username = data[0].upper()
						first_name = data[1].title()
						try:
							email = data[2].lower()
						except:
							email = data[2]
						is_active = False
						if data[3].upper() == 'Y':
							is_active = True
						phone = data[4]
						sem = Semester.objects.get(sem=data[5])
						sec = data[6].upper()
						department = request.user.department
						ug = False
						if data[7].upper() == 'Y':
							ug = True
						user_type = UserType.objects.get(name="Student")

						# Check if Batch is null
						batch = None
						is_null = False

						try:
							is_null = math.isnan(float(data[8]))
						except:
							is_null = False

						if not is_null:
							batch = data[8].upper()

						# Check if Sub Batch is null
						sub_batch = None
						try:
							is_null = math.isnan(float(data[9]))
						except:
							is_null = False
						if not is_null:
							sub_batch = data[9].upper()

						# Check if elecitves exists

						elective_1 = None
						is_null = False

						try:
							is_null = math.isnan(float(data[10]))
						except:
							is_null = False

						if not is_null:
							elective_1 = data[10].upper()

						elective_2 = None
						is_null = False

						try:
							is_null = math.isnan(float(data[11]))
						except:
							is_null = False

						if not is_null:
							elective_2 = data[11].upper()

						if data[12].upper() == 'Y':
							done = True
						else:
							done = False

						# print("Entered 3", username)
						user_obj = User.objects.create(username=username, password=password, first_name=first_name, email=email, is_active=is_active, phone=phone, sem=str(sem), sec=sec, department=department, ug=ug, batch=batch, sub_batch=sub_batch, done=done)

						user_obj.user_type.add(user_type)

						electives = []
						if elective_1:
							electives.append(Subject.objects.get(code=elective_1))
						if elective_2:
							electives.append(Subject.objects.get(code=elective_2))

						user_obj.elective.add(*electives)

						user_obj.save()

						added.append(data)

		except Exception as e:
			errors.append(e)

		context = {
		"errors":errors,
		"updated":updated,
		"added":added,
		"users":True,
		'form': FileUploadForm(),
		}
		# print(data)
	else:
		context = {
		'form': FileUploadForm(),
		}
	return render(request, template_name, context)

@login_required
def easy_upload(request):
	"""
	"""

	template_name = "easy_upload/home.html"
	if request.user.groups.filter(name='feedback_admin').exists():

		if request.user.is_superuser:
			departments = Department.objects.filter(d_type="teaching").order_by('id').values('name').distinct()
		else:
			department = request.user.department
		completed = {}
		total = 0

		if request.user.is_superuser:
			for dept in departments:

				completed[dept['name']] = User.objects.filter(department__name=dept['name'], is_active=True, user_type__name="Student", done=False).count()
				total += completed[dept['name']]
		else:
			completed[department] = User.objects.filter(department__name=department, is_active=True, user_type__name="Student").count()

		context = {
				"home":True,
				"completed":completed,
				"total": total,
		}
		return render(request, template_name, context)
	else:
		return HttpResponseRedirect('/dashboard')

@login_required
def easy_upload_test(request):
	"""
	"""

	template_name = "easy_upload/test.html"
	if request.user.groups.filter(name='feedback_admin').exists():

		dept = request.user.department

		semester = Teaches.objects.filter(department=dept).order_by('sem').values('sem').distinct()
		section = Teaches.objects.filter(department=dept).order_by('sec').values('sec').distinct()
		data = {}

		for sem in semester:

			for sec in section:
				if Teaches.objects.filter(department=dept, sem=sem['sem'], sec=sec['sec']).exists():
					if sem['sem'] in data:
						data[sem['sem']][sec['sec']] = Teaches.objects.filter(department=dept, sem=sem['sem'], sec=sec['sec'])
					else:
						data[sem['sem']] = {sec['sec']:Teaches.objects.filter(department=dept, sem=sem['sem'], sec=sec['sec']),}

		context = {
				"test":True,
				"data":data,
		}
		return render(request, template_name, context)
	else:
		return HttpResponseRedirect('/dashboard')

@login_required
def easy_upload_message(request):
	"""
	"""

	template_name = "easy_upload/message.html"

	if request.method == 'POST':

		errors = []
		updated = []
		form = MessageForm(request.POST)
		count, n_count = 0, 0
		if form.is_valid():
			text = form.cleaned_data['message_text']

		try:
			user_data = User.objects.filter(department=request.user.department, done=False, is_active=True)

			for data in user_data:
				try:
					if data.phone:
						phone1 = data.phone
						message = "Dear %s,\n\n%s\n\nyour USN: %s\nregards,\nHoD %s" %(data.first_name, text, data.username, data.department)
						# print(message)
						params = {"number": phone1, "text": message}
						baseUrl = (
							"https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey=62sxGWT6MkCjDul6eNKejw&senderid=BMSITM&channel=2&DCS=0&flashsms=0&"
							+ ap.urlencode(params)
						)
						urllib.request.urlopen(baseUrl).read(1000)
						count += 1
					else:
						n_count += 1
				except Exception as e:
					errors.append("couldn't send message to %s. cause: %s" %(data.username, e))

			updated.append("Message sent to %d students." %(count))
			updated.append("Could not send message to %d students." %(n_count))

			context = {
				"errors":errors,
				"updated":updated,
				"message":True,
				'form': MessageForm(),
			}

			message = form.save(commit=False)
			message.sent_by = request.user

			message.save()


		except Exception as e:
			errors.append("Exception, cause: %s" %(e) )
	else:
		context = {
		'form': MessageForm(),
		}
	return render(request, template_name, context)

@login_required
def test_mode(request):
	"""
	"""
	if request.user.groups.filter(name='feedback_admin').exists():
		department = Department.objects.get(id=request.user.department.id)

		if department.test_mode:
			department.test_mode=False
			department.save()
		else:
			department.test_mode=True
			department.save()

		return HttpResponseRedirect('/easy-upload/settings')

	else:
		return HttpResponseRedirect('/dashboard')

@login_required
def teachers_list(request):
	"""
	"""
	if request.user.groups.filter(name='feedback_admin').exists():


		template_name = "easy_upload/teachers_list.html"
		teachers = User.objects.filter(department=request.user.department, user_type__name="Faculty")
		context = {'teachers_list': teachers}

		return render(request, template_name, context)

	else:
		return HttpResponseRedirect('/dashboard')

@login_required
def easy_upload_settings(request):
	"""
	"""

	template_name = "easy_upload/settings.html"
	if request.user.groups.filter(name='feedback_admin').exists():
		current_process = FeedbackProcess.objects.all().order_by('-id')[0]
		
		context = {
				"settings":True,
				"current_process":current_process,
				"form": FeedbackProcessForm(),
		}

		if request.method == 'POST':
			form = FeedbackProcessForm(request.POST)
			if form.is_valid():
				# Generate consolidated report for the last time
				data = User.objects.filter(user_type__name="Faculty")

				for teacher in data:
					try:
						r = requests.get(
							"https://feedback360.bmsit.ac.in/__/__/--/__/__sreports/%s/" % (teacher.username)
						)
						count += 1
					except:
						pass

				# Deleting all answers
				StudentAnswer.objects.all().delete()

				# Creating new process
				process = form.save()
				title = form.cleaned_data['title']
				current_process = FeedbackProcess.objects.all().order_by('-id')[0]
				context['current_process'] = current_process
				messages.success(request, "All student answers deleted and a new process '%s' Started" %(title))
			return render(request, template_name, context)
		else:
			return render(request, template_name, context)
	else:
		return HttpResponseRedirect('/dashboard')
