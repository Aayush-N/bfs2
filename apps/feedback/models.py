from django.db import models
from django.contrib.auth import get_user_model

import datetime
from datetime import date


class FeedbackForm(models.Model):
    """
	Feedback Form: Stores the feedback form for the respective type of user
	As each type of user has different forms to be displayed, we store the below boolean values
	"""

    title = models.CharField("Form Title", max_length=50)
    description = models.CharField("Form Description", max_length=250)

    # The type of user that is allowed to give the feedback for this form
    user_type = models.ManyToManyField(
        "general.UserType",
        help_text="Type of user that is allowed to give the feedback for this form",
    )

    # The code of the form
    code = models.CharField(
        "Form Code",
        max_length=2,
        help_text="Mandatory to enter two characters",
        null=False,
        blank=False,
    )

    # The type of the user that will receive feedback through this form
    recipient = models.ForeignKey(
        "general.UserType",
        help_text="Type of user that is receiving the feedback for this form",
        related_name="form",
        null=True,
    )

    active = models.BooleanField(default=True)

    def __str__(self):
    	return str(self.title)


class Question(models.Model):
    """
	Question: Holds the questions for respective user type
	"""

    form = models.ForeignKey(
        "FeedbackForm", on_delete=models.CASCADE, related_name="question"
    )
    text = models.TextField("Question")

    def __str__(self):
    	return str(self.text)


class Answer(models.Model):
    """
	Answers: If the student is giving the feedback for a teacher, it gets stored for the teacher,
	which holds the details from the table - teaches. So, we can obtain all details such as Sem, Sec
	from it while generation of reports.

	If the feedback is to anyone else, it will get stored to the User.
	"""

    question = models.ForeignKey("question")
    teacher = models.ForeignKey("general.teaches", null=True)

    ANSWER_CHOICES = [
        ("Excellent", "Excellent"),
        ("Good", "Good"),
        ("Satisfactory", "Satisfactory"),
        ("Poor", "Poor"),
        ("Very Poor", "Very Poor"),
    ]
    value = models.CharField(max_length=50, choices=ANSWER_CHOICES)

    form = models.ForeignKey("feedbackform", null=True)
    recipient = models.ForeignKey(get_user_model(), null=True)

    def __str__(self):
        return self.question.text + " (" + str(self.value) + ")"


class StudentAnswer(models.Model):
    """
	Answers: If the student is giving the feedback for a teacher, it gets stored for the teacher,
	which holds the details from the table - teaches. So, we can obtain all details such as Sem, Sec
	from it while generation of reports.

	If the feedback is to anyone else, it will get stored to the User.
	"""
    question = models.ForeignKey("question")
    teacher = models.ForeignKey("general.teaches", null=True)

    ANSWER_CHOICES = [
        ("Excellent", "Excellent"),
        ("Good", "Good"),
        ("Satisfactory", "Satisfactory"),
        ("Poor", "Poor"),
        ("Very Poor", "Very Poor"),
    ]
    value = models.CharField(max_length=60, choices=ANSWER_CHOICES)

    form = models.ForeignKey("feedbackform", null=True)
    recipient = models.ForeignKey(get_user_model(), null=True)

    def __str__(self):
        try:
            return self.teacher.teacher.first_name
        except:
            return str(self.value)


class ConsolidatedReport(models.Model):
    """
	The consolidated report is stored in this table.
	"""

    teacher = models.ForeignKey("general.User", null=True, blank=True)
    form_name = models.CharField("Name of the form", max_length=100)
    total = models.CharField("Total value they got", max_length=10)
    process = models.ForeignKey("FeedbackProcess", null=True, blank=True)

    def __str__(self):
        return self.form_name


class StudentConsolidatedReport(models.Model):
    """
	The Student consolidated report is stored in this table.
	"""

    teacher = models.ForeignKey("general.User", null=True, blank=True)
    total = models.FloatField("Total value they got", max_length=10, null=True, blank=True)
    department = models.ForeignKey("general.Department", null=True, blank=True)

    subject = models.CharField("Student's subject", max_length=256, null=True, blank=True)
    sem = models.IntegerField("Student's Semester", max_length=10, null=True, blank=True)
    sec = models.CharField("Student's Section", max_length=50, null=True, blank=True)
    batch = models.CharField("Student's Batch", max_length=50, null=True, blank=True)
    sub_batch = models.CharField(
        "Student's sub batch", max_length=50, null=True, blank=True
    )
    ug = models.BooleanField(default=False)
    count = models.IntegerField("No. of students",null=True, blank=True)
    date_created = models.DateField(auto_now_add=True, blank=True)
    process = models.ForeignKey("FeedbackProcess", null=True, blank=True)

    def __str__(self):
        return self.teacher.first_name + " | "+self.subject + " [" + str(self.count) + "]"

def current_years():
    return date.today().year

class FeedbackProcess(models.Model):
    """
    """

    current_year = current_years()

    title = models.CharField("Feedback Title", max_length=250)
    date = models.DateField("Date", auto_now_add=True, blank=True, null=True)
    p2p = models.BooleanField("Peer to peer", default=False)

    def __str__(self):
        return self.title