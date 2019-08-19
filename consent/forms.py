from django.forms import ModelForm
from consent.models import Consent

class ConsentForm(ModelForm):

    class Meta:
        model = Consent
        exclude = []

    def clean(self):
        cleaned_data = super().clean()

