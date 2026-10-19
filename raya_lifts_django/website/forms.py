from django import forms
from .models import Enquiry

class EnquiryForm(forms.ModelForm):
    # Honeypot field: bots often fill every field; real users leave it blank.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Enquiry
        fields = ["name", "phone", "email", "city", "lift_interest", "message", "privacy_consent"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone number", "autocomplete": "tel"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email address", "autocomplete": "email"}),
            "city": forms.TextInput(attrs={"placeholder": "City"}),
            "lift_interest": forms.TextInput(attrs={"placeholder": "Lift type you are interested in"}),
            "message": forms.Textarea(attrs={"placeholder": "Tell us a little about your requirement", "rows": 5}),
            "privacy_consent": forms.CheckboxInput(),
        }

    def clean_website(self):
        value = self.cleaned_data.get("website", "")
        if value:
            raise forms.ValidationError("Invalid submission.")
        return value
