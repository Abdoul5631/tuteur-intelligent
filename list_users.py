#!/usr/bin/env python
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

print('👥 Users in database:\n' + '='*60)

users = User.objects.all().values('id', 'username', 'email', 'is_active', 'is_staff')

if users:
    for user in users:
        status = '✓ Active' if user['is_active'] else '✗ Inactive'
        print(f"  ID: {user['id']:3d} | {user['username']:20s} | {user['email']:30s} | {status}")
else:
    print("  ⚠ No users found in database")

print(f"\nTotal: {users.count()} user(s)")

# Check for Madi specifically
madi = User.objects.filter(username__iexact='madi').first()
if madi:
    print(f"\n✓ 'Madi' user found!")
    print(f"  Username: {madi.username}")
    print(f"  Email: {madi.email}")
    print(f"  Active: {madi.is_active}")
else:
    print(f"\n✗ 'Madi' user NOT found in database")
