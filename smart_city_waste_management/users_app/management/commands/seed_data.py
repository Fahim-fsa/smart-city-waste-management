from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from citizen_reports_app.models import WasteReport
from waste_management_app.models import VolunteerTask
from notifications_app.models import Notification
from analytics_app.models import AnalyticsReport

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create superuser / admin
        if not User.objects.filter(email='admin@smartwaste.com').exists():
            admin = User.objects.create_superuser(
                email='admin@smartwaste.com',
                password='admin123',
                name='System Admin',
                phone='01700000001',
                address='City Hall, Smart City',
                role='admin',
            )
            self.stdout.write(self.style.SUCCESS('  Created admin: admin@smartwaste.com / admin123'))
        else:
            admin = User.objects.get(email='admin@smartwaste.com')

        # Citizens
        citizens = []
        citizen_data = [
            ('Rahim Uddin', 'rahim@example.com', '01711111111', 'Mirpur, Dhaka'),
            ('Sumaiya Khan', 'sumaiya@example.com', '01722222222', 'Gulshan, Dhaka'),
            ('Karim Hossain', 'karim@example.com', '01733333333', 'Dhanmondi, Dhaka'),
        ]
        for name, email, phone, address in citizen_data:
            if not User.objects.filter(email=email).exists():
                u = User.objects.create_user(
                    email=email, password='password123',
                    name=name, phone=phone, address=address, role='citizen'
                )
                citizens.append(u)
                self.stdout.write(f'  Created citizen: {email} / password123')
            else:
                citizens.append(User.objects.get(email=email))

        # Volunteers
        volunteers = []
        vol_data = [
            ('Nasrin Akter', 'nasrin@example.com', '01755555555', 'Uttara, Dhaka'),
            ('Farhan Islam', 'farhan@example.com', '01766666666', 'Mohammadpur, Dhaka'),
        ]
        for name, email, phone, address in vol_data:
            if not User.objects.filter(email=email).exists():
                u = User.objects.create_user(
                    email=email, password='password123',
                    name=name, phone=phone, address=address, role='volunteer'
                )
                volunteers.append(u)
                self.stdout.write(f'  Created volunteer: {email} / password123')
            else:
                volunteers.append(User.objects.get(email=email))

        # Driver
        if not User.objects.filter(email='driver@example.com').exists():
            driver = User.objects.create_user(
                email='driver@example.com', password='password123',
                name='Raju Driver', phone='01788888888',
                address='Kamrangirchar, Dhaka', role='driver'
            )
            self.stdout.write('  Created driver: driver@example.com / password123')
        else:
            driver = User.objects.get(email='driver@example.com')

        # Waste Reports
        reports_data = [
            (citizens[0], 'Illegal Dumping at Mirpur Road', 'Large pile of household waste left on the footpath near bus stop.', 'Mirpur Road, Section 10, Dhaka', 'approved'),
            (citizens[0], 'Overflowing Garbage Bin', 'The public bin at the market has been overflowing for 3 days.', 'Mirpur Bazar, Dhaka', 'pending'),
            (citizens[1], 'Construction Waste Blocking Road', 'Debris from a nearby construction site is blocking half the road.', 'Gulshan 2 Circle, Dhaka', 'completed'),
            (citizens[1], 'Waste in Drainage Canal', 'Residents are throwing waste into the drainage canal causing blockage.', 'Gulshan Lake Area, Dhaka', 'assigned'),
            (citizens[2], 'Burnt Waste Pile', 'Someone set fire to a waste pile causing smoke in the area.', 'Dhanmondi 32, Dhaka', 'in_progress'),
            (citizens[2], 'Stray Dogs Scattering Garbage', 'Stray dogs tearing open garbage bags on the main street.', 'Dhanmondi 15, Dhaka', 'rejected'),
        ]

        created_reports = []
        for citizen, title, desc, location, status in reports_data:
            if not WasteReport.objects.filter(title=title).exists():
                report = WasteReport.objects.create(
                    citizen=citizen,
                    title=title,
                    description=desc,
                    location=location,
                    status=status,
                    approved_by=admin if status not in ['pending', 'rejected'] else None,
                )
                created_reports.append(report)
                self.stdout.write(f'  Created report: {title}')
            else:
                created_reports.append(WasteReport.objects.get(title=title))

        # Volunteer Tasks
        task_pairs = [
            (created_reports[0], volunteers[0], 'completed'),
            (created_reports[3], volunteers[1], 'in_progress'),
            (created_reports[4], volunteers[0], 'accepted'),
        ]
        for report, volunteer, status in task_pairs:
            if not VolunteerTask.objects.filter(report=report, volunteer=volunteer).exists():
                VolunteerTask.objects.create(
                    report=report,
                    volunteer=volunteer,
                    assigned_by=admin,
                    status=status,
                    notes='Please complete this cleanup as soon as possible.',
                )
                self.stdout.write(f'  Created task for report: {report.title}')

        # Notifications
        for citizen in citizens:
            if not Notification.objects.filter(user=citizen, title='Welcome!').exists():
                Notification.objects.create(
                    user=citizen,
                    title='Welcome!',
                    message='Welcome to Smart City Waste Management. Help us keep our city clean!',
                    notification_type='system',
                )

        for vol in volunteers:
            if not Notification.objects.filter(user=vol, title='Welcome Volunteer!').exists():
                Notification.objects.create(
                    user=vol,
                    title='Welcome Volunteer!',
                    message='Thank you for joining as a volunteer. You make a real difference!',
                    notification_type='system',
                )

        # Analytics Report
        if not AnalyticsReport.objects.filter(area_name='Dhaka City').exists():
            AnalyticsReport.objects.create(
                area_name='Dhaka City',
                total_reports=WasteReport.objects.count(),
                completed_reports=WasteReport.objects.filter(status='completed').count(),
                pending_reports=WasteReport.objects.filter(status='pending').count(),
                active_volunteers=User.objects.filter(role='volunteer').count(),
            )
            self.stdout.write('  Created analytics report for Dhaka City')

        # Reward points
        citizens[0].reward_points = 50
        citizens[0].save()
        citizens[1].reward_points = 80
        citizens[1].save()
        volunteers[0].reward_points = 150
        volunteers[0].save()
        volunteers[1].reward_points = 100
        volunteers[1].save()

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!\n'))
        self.stdout.write('Login credentials:')
        self.stdout.write('  Admin:     admin@smartwaste.com   / admin123')
        self.stdout.write('  Citizen:   rahim@example.com      / password123')
        self.stdout.write('  Volunteer: nasrin@example.com     / password123')
        self.stdout.write('  Driver:    driver@example.com     / password123')
