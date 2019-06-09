from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Message, Department, Semester
import string


class LoginForm(AuthenticationForm):
    """
	Form for taking Username and password
	"""

    username = forms.CharField(
        label="usn",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "name": "usn1",
                "id": "usn",
                "placeholder": "Enter USN",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        max_length=30,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "name": "otp",
                "id": "otp",
                "placeholder": "Enter OTP",
            }
        ),
    )

class DoneChangeForm(forms.Form):
    """docstring for DoneChangeForm"""

    SEC_CHOICE = ((x, x) for x in string.ascii_uppercase)
    SEM_CHOICE = ((x, x) for x in range(1,9))

    department = forms.ModelMultipleChoiceField(queryset=Department.objects.all())
    sem = forms.MultipleChoiceField(choices=SEM_CHOICE)
    sec = forms.MultipleChoiceField(choices=SEC_CHOICE)
    val = forms.BooleanField(required=False)
        

class FileUploadForm(forms.Form):
    file = forms.FileField()

    def clean(self):
        cleaned_data = super(FileUploadForm, self).clean()
        file = cleaned_data.get('file')

class MessageForm(forms.ModelForm):
    
    class Meta:
        model = Message
        exclude = ['sent_by', 'time_stamp']