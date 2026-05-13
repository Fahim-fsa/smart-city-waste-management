from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileEditForm, ChangePasswordForm
from .models import User
from citizen_reports_app.models import WasteReport
from waste_management_app.models import VolunteerTask
from notifications_app.models import Notification


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.name}! Registration successful.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'users_app/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'users_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'users_app/profile.html', {'user': request.user})


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users_app/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data['old_password']):
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Old password is incorrect.')
    else:
        form = ChangePasswordForm()
    return render(request, 'users_app/change_password.html', {'form': form})


@login_required
def dashboard_view(request):
    user = request.user
    context = {'user': user}

    if user.role == 'admin':
        context['total_reports'] = WasteReport.objects.count()
        context['pending_reports'] = WasteReport.objects.filter(status='pending').count()
        context['completed_reports'] = WasteReport.objects.filter(status='completed').count()
        context['total_users'] = User.objects.count()
        context['total_volunteers'] = User.objects.filter(role='volunteer').count()
        context['recent_reports'] = WasteReport.objects.order_by('-report_date')[:5]
        context['recent_users'] = User.objects.order_by('-date_joined')[:5]
        return render(request, 'users_app/admin_dashboard.html', context)

    elif user.role == 'volunteer':
        context['my_tasks'] = VolunteerTask.objects.filter(volunteer=user).count()
        context['completed_tasks'] = VolunteerTask.objects.filter(volunteer=user, status='completed').count()
        context['pending_tasks'] = VolunteerTask.objects.filter(volunteer=user, status__in=['assigned', 'accepted', 'in_progress']).count()
        context['recent_tasks'] = VolunteerTask.objects.filter(volunteer=user).order_by('-assigned_date')[:5]
        return render(request, 'users_app/volunteer_dashboard.html', context)

    else:  # citizen
        context['my_reports'] = WasteReport.objects.filter(citizen=user).count()
        context['pending_reports'] = WasteReport.objects.filter(citizen=user, status='pending').count()
        context['completed_reports'] = WasteReport.objects.filter(citizen=user, status='completed').count()
        context['recent_reports'] = WasteReport.objects.filter(citizen=user).order_by('-report_date')[:5]
        context['reward_points'] = user.reward_points
        return render(request, 'users_app/citizen_dashboard.html', context)
