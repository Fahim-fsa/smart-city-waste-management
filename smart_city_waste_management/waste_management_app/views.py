from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import VolunteerTask
from .forms import VolunteerTaskForm, TaskUpdateForm
from notifications_app.models import Notification
from citizen_reports_app.models import WasteReport


@login_required
def task_list_view(request):
    user = request.user
    if user.role == 'admin':
        tasks = VolunteerTask.objects.all()
    else:
        tasks = VolunteerTask.objects.filter(volunteer=user)
    return render(request, 'waste_management_app/task_list.html', {'tasks': tasks})


@login_required
def task_detail_view(request, pk):
    task = get_object_or_404(VolunteerTask, pk=pk)
    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            updated_task = form.save(commit=False)
            if updated_task.status == 'completed':
                updated_task.completion_date = timezone.now()
                task.volunteer.reward_points += 50
                task.volunteer.save()
                updated_task.report.status = 'completed'
                updated_task.report.save()
                Notification.objects.create(
                    user=task.report.citizen,
                    title='Cleanup Completed',
                    message=f'The cleanup for your report "{task.report.title}" has been completed!',
                    notification_type='report_update'
                )
            updated_task.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('task_detail', pk=pk)
    else:
        form = TaskUpdateForm(instance=task)
    return render(request, 'waste_management_app/task_detail.html', {'task': task, 'form': form})


@login_required
def task_form_view(request):
    if request.user.role != 'admin':
        messages.error(request, 'Permission denied.')
        return redirect('task_list')
    if request.method == 'POST':
        form = VolunteerTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()
            task.report.status = 'assigned'
            task.report.save()
            Notification.objects.create(
                user=task.volunteer,
                title='New Task Assigned',
                message=f'You have been assigned to clean up: {task.report.title}',
                notification_type='task_assignment'
            )
            messages.success(request, 'Task assigned successfully.')
            return redirect('task_list')
    else:
        form = VolunteerTaskForm()
    return render(request, 'waste_management_app/task_form.html', {'form': form})


@login_required
def task_history_view(request):
    tasks = VolunteerTask.objects.filter(volunteer=request.user, status='completed')
    return render(request, 'waste_management_app/task_history.html', {'tasks': tasks})
