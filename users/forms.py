
from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'sex', 'location']

    def clean_location(self):
        location = self.cleaned_data['location']
        if location.type != 'CELL':  # Changed to CELL
            raise forms.ValidationError("Please select down to the Cell level.")
        return location