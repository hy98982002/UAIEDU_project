#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uai_backend.settings')
django.setup()

from apps.users.models import User

# 检查目标用户
user = User.objects.get(phone="18512292333")
print(f"手机号: {user.phone}")
print(f"密码字段: {repr(user.password)}")
print(f"has_usable_password(): {user.has_usable_password()}")
print(f"密码是否以!开头: {user.password.startswith('!')}") 