from django import forms
from .models import VolunteerTask
from users_app.models import User
from citizen_reports_app.models import WasteReport


class VolunteerTaskForm(forms.ModelForm):
    class Meta:
        model = VolunteerTask
        fields = ['report', 'volunteer', 'notes']
        widgets = {
            'report': forms.Select(attrs={'class': 'form-control'}),
            'volunteer': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['volunteer'].queryset = User.objects.filter(role='volunteer')
        self.fields['report'].queryset = WasteReport.objects.filter(status='approved')


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = VolunteerTask
        fields = ['status', 'notes', 'before_cleanup_image', 'after_cleanup_image']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'before_cleanup_image': forms.FileInput(attrs={'class': 'form-control'}),
            'after_cleanup_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
