from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import AnalyticsReport
from citizen_reports_app.models import WasteReport
from users_app.models import User
from waste_management_app.models import VolunteerTask


class AnalyticsForm(forms.ModelForm):
    class Meta:
        model = AnalyticsReport
        fields = ['area_name']
        widgets = {
            'area_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Area Name'}),
        }


@login_required
def analytics_dashboard_view(request):
    if request.user.role != 'admin':
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')

    total_reports = WasteReport.objects.count()
    completed_reports = WasteReport.objects.filter(status='completed').count()
    pending_reports = WasteReport.objects.filter(status='pending').count()
    total_users = User.objects.count()
    total_volunteers = User.objects.filter(role='volunteer').count()
    total_citizens = User.objects.filter(role='citizen').count()
    total_tasks = VolunteerTask.objects.count()
    completed_tasks = VolunteerTask.objects.filter(status='completed').count()
    analytics_reports = AnalyticsReport.objects.all()[:10]

    # Leaderboard
    leaderboard = User.objects.filter(role__in=['citizen', 'volunteer']).order_by('-reward_points')[:10]

    context = {
        'total_reports': total_reports,
        'completed_reports': completed_reports,
        'pending_reports': pending_reports,
        'total_users': total_users,
        'total_volunteers': total_volunteers,
        'total_citizens': total_citizens,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'analytics_reports': analytics_reports,
        'leaderboard': leaderboard,
    }
    return render(request, 'analytics_app/analytics_dashboard.html', context)


@login_required
def generate_report_view(request):
    if request.user.role != 'admin':
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = AnalyticsForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            area = report.area_name
            report.total_reports = WasteReport.objects.count()
            report.completed_reports = WasteReport.objects.filter(status='completed').count()
            report.pending_reports = WasteReport.objects.filter(status='pending').count()
            report.active_volunteers = User.objects.filter(role='volunteer').count()
            report.save()
            messages.success(request, f'Analytics report for "{area}" generated successfully.')
            return redirect('analytics_dashboard')
    else:
        form = AnalyticsForm()
    return render(request, 'analytics_app/report_generation.html', {'form': form})
