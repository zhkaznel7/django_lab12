from django import forms

from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "priority")
        widgets = {"description": forms.Textarea(attrs={"rows": 5})}

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 5:
            raise forms.ValidationError("Тақырып кемінде 5 таңбадан тұруы керек.")
        return title
