#!/usr/bin/env python
"""
修复空密码用户脚本
将密码字段为空但has_usable_password()返回True的用户修复为真正的不可用密码状态
"""

import os
import sys
import django

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uai_backend.settings')
django.setup()

from apps.users.models import User

def fix_empty_password_users():
    """修复空密码用户"""
    print("=" * 60)
    print("UAI教育平台 - 修复空密码用户")
    print("=" * 60)
    
    # 查找密码字段为空但has_usable_password返回True的用户
    problematic_users = []
    
    for user in User.objects.all():
        if user.password == '' and user.has_usable_password():
            problematic_users.append(user)
    
    if not problematic_users:
        print("✅ 没有发现需要修复的用户")
        return
    
    print(f"🔍 发现 {len(problematic_users)} 个需要修复的用户:")
    
    for i, user in enumerate(problematic_users, 1):
        print(f"  {i}. 手机号: {user.phone}")
        print(f"     密码字段: {repr(user.password)}")
        print(f"     has_usable_password(): {user.has_usable_password()}")
        
        # 修复：设置为不可用密码
        user.set_unusable_password()
        user.save()
        
        print(f"     修复后 has_usable_password(): {user.has_usable_password()}")
        print(f"     修复后密码字段: {repr(user.password)}")
        print("     ✅ 已修复")
        print("-" * 40)
    
    print(f"✅ 成功修复 {len(problematic_users)} 个用户")

if __name__ == "__main__":
    fix_empty_password_users() 