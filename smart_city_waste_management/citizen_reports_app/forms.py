from django import forms
from .models import WasteReport


class WasteReportForm(forms.ModelForm):
    class Meta:
        model = WasteReport
        fields = ['title', 'description', 'image', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Report Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the issue...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location / Area'}),
        }


class ReportStatusForm(forms.ModelForm):
    class Meta:
        model = WasteReport
        fields = ['status', 'completion_image']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'completion_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
