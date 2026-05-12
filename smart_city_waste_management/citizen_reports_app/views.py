from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import WasteReport
from .forms import WasteReportForm, ReportStatusForm
from notifications_app.models import Notification


@login_required
def report_form_view(request):
    if request.method == 'POST':
        form = WasteReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.citizen = request.user
            report.save()
            # Add reward points
            request.user.reward_points += 10
            request.user.save()
            # Create notification
            Notification.objects.create(
                user=request.user,
                title='Report Submitted',
                message=f'Your report "{report.title}" has been submitted successfully.',
                notification_type='report_update'
            )
            messages.success(request, 'Waste report submitted successfully! You earned 10 reward points.')
            return redirect('report_list')
    else:
        form = WasteReportForm()
    return render(request, 'citizen_reports_app/report_form.html', {'form': form})


@login_required
def report_list_view(request):
    user = request.user
    if user.role == 'admin':
        reports = WasteReport.objects.all()
    else:
        reports = WasteReport.objects.filter(citizen=user)

    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    if search:
        reports = reports.filter(title__icontains=search)
    if status_filter:
        reports = reports.filter(status=status_filter)

    paginator = Paginator(reports, 10)
    page = request.GET.get('page')
    reports = paginator.get_page(page)
    return render(request, 'citizen_reports_app/report_list.html', {'reports': reports, 'search': search, 'status_filter': status_filter})


@login_required
def report_detail_view(request, pk):
    report = get_object_or_404(WasteReport, pk=pk)
    return render(request, 'citizen_reports_app/report_detail.html', {'report': report})


@login_required
def report_history_view(request):
    reports = WasteReport.objects.filter(citizen=request.user)
    return render(request, 'citizen_reports_app/report_history.html', {'reports': reports})


@login_required
def report_approve_view(request, pk):
    if request.user.role != 'admin':
        messages.error(request, 'Permission denied.')
        return redirect('report_list')
    report = get_object_or_404(WasteReport, pk=pk)
    report.status = 'approved'
    report.approved_by = request.user
    report.save()
    Notification.objects.create(
        user=report.citizen,
        title='Report Approved',
        message=f'Your report "{report.title}" has been approved.',
        notification_type='report_update'
    )
    messages.success(request, 'Report approved.')
    return redirect('report_detail', pk=pk)


@login_required
def report_reject_view(request, pk):
    if request.user.role != 'admin':
        messages.error(request, 'Permission denied.')
        return redirect('report_list')
    report = get_object_or_404(WasteReport, pk=pk)
    report.status = 'rejected'
    report.approved_by = request.user
    report.save()
    Notification.objects.create(
        user=report.citizen,
        title='Report Rejected',
        message=f'Your report "{report.title}" has been reviewed and rejected.',
        notification_type='report_update'
    )
    messages.warning(request, 'Report rejected.')
    return redirect('report_detail', pk=pk)
