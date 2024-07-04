from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Contact
from django.forms import widgets



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ("timestamp",)
        widgets = {
            "name": widgets.TextInput(attrs={"class": "required form-control","required": True,"placeholder": "Name"}),
            "phone": widgets.TextInput(attrs={"class": "required form-control", "required": True,"placeholder": "Phone Number"}),
            "email": widgets.EmailInput(attrs={"class": "required form-control","required": True,"placeholder": "Email"}),
            "message": widgets.Textarea(attrs={"class": "required form-control","required": True,"placeholder": "Message"}),
        }
