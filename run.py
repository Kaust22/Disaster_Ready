#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disaster_prep.settings')
    
    # Setup Django
    django.setup()
    
    # Run migrations
    from django.core.management import call_command
    call_command('migrate', interactive=False)
    
    # Create superuser if it doesn't exist
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Created superuser: admin/admin123")
    
    # Populate initial data
    try:
        call_command('populate_data')
        print("Initial data populated successfully")
    except Exception as e:
        print(f"Data population status: {str(e)}")
    
    # Start the development server using standard Django approach
    print("Starting Django development server...")
    sys.argv = ['run.py', 'runserver', '0.0.0.0:5000']
    execute_from_command_line(sys.argv)