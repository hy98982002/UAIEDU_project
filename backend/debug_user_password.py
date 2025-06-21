#!/usr/bin/env python
"""
用户密码状态调试脚本
用于检查注册用户的密码设置状态
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

def check_user_password_status():
    """检查所有用户的密码状态"""
    print("=" * 60)
    print("UAI教育平台 - 用户密码状态检查报告")
    print("=" * 60)
    
    users = User.objects.all()
    
    if not users.exists():
        print("❌ 数据库中没有用户")
        return
    
    print(f"📊 总用户数: {users.count()}")
    print("-" * 60)
    
    for i, user in enumerate(users, 1):
        print(f"👤 用户 #{i}")
        print(f"   手机号: {user.phone}")
        print(f"   唯一标识: {user.unique_identifier}")
        print(f"   密码字段: {repr(user.password)}")
        print(f"   has_usable_password(): {user.has_usable_password()}")
        print(f"   check_password(''): {user.check_password('')}")
        print(f"   is_phone_verified: {user.is_phone_verified}")
        print(f"   注册时间: {user.add_time}")
        print(f"   是否激活: {user.is_active}")
        print("-" * 40)
    
    # 重点检查手机号为 18512292333 的用户
    target_phone = "18512292333"
    target_user = users.filter(phone=target_phone).first()
    
    if target_user:
        print("🎯 重点检查用户 18512292333:")
        print(f"   ID: {target_user.id}")
        print(f"   密码原始值: {repr(target_user.password)}")
        print(f"   密码长度: {len(target_user.password) if target_user.password else 0}")
        print(f"   has_usable_password(): {target_user.has_usable_password()}")
        
        # 检查密码是否以 pbkdf2_ 开头（Django加密密码格式）
        if target_user.password:
            if target_user.password.startswith('pbkdf2_'):
                print("   ✅ 密码已加密（已设置密码）")
            elif target_user.password.startswith('!'):
                print("   ❌ 密码不可用（未设置密码）") 
            else:
                print(f"   ⚠️  密码格式异常: {target_user.password[:20]}...")
        else:
            print("   ❌ 密码字段为空")
            
        print("-" * 40)
    else:
        print(f"❌ 未找到手机号为 {target_phone} 的用户")

def create_test_user():
    """创建一个测试用户（无密码）"""
    test_phone = "18512292334"
    
    # 检查是否已存在
    if User.objects.filter(phone=test_phone).exists():
        print(f"❌ 测试用户 {test_phone} 已存在")
        return
    
    # 创建用户（不设置密码）
    user = User.objects.create(
        phone=test_phone,
        is_phone_verified=True,
    )
    
    print(f"✅ 创建测试用户成功:")
    print(f"   手机号: {user.phone}")
    print(f"   密码字段: {repr(user.password)}")
    print(f"   has_usable_password(): {user.has_usable_password()}")

if __name__ == "__main__":
    print("🔍 开始检查用户密码状态...")
    check_user_password_status()
    
    print("\n" + "=" * 60)
    print("🔧 创建测试用户（无密码）...")
    create_test_user()
    
    print("\n" + "=" * 60)
    print("✅ 检查完成！") 