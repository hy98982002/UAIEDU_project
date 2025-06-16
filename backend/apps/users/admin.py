from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    """
    用户管理后台配置
    """
    # 列表页显示的字段
    list_display = [
        'phone', 'nickname', 'email', 'is_active', 
        'is_staff', 'is_deleted', 'add_time', 'last_login'
    ]
    
    # 可以点击进入详情页的字段
    list_display_links = ['phone', 'nickname']
    
    # 右侧过滤器
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 
        'is_deleted', 'gender', 'add_time'
    ]
    
    # 搜索字段
    search_fields = ['phone', 'nickname', 'email', 'username']
    
    # 分页设置
    list_per_page = 20
    
    # 详情页字段分组
    fieldsets = (
        ('基本信息', {
            'fields': ('phone', 'username', 'nickname', 'email')
        }),
        ('个人资料', {
            'fields': ('avatar', 'gender', 'birthday', 'bio'),
            'classes': ('collapse',)
        }),
        ('权限设置', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('系统信息', {
            'fields': ('last_login', 'last_login_ip', 'add_time', 'update_time', 'is_deleted'),
            'classes': ('collapse',)
        }),
    )
    
    # 只读字段
    readonly_fields = ['add_time', 'update_time', 'last_login']
    
    # 批量操作
    actions = ['soft_delete_users', 'activate_users']
    
    def soft_delete_users(self, request, queryset):
        """批量软删除用户"""
        count = queryset.update(is_deleted=True, is_active=False)
        self.message_user(request, f'成功软删除 {count} 个用户。')
    soft_delete_users.short_description = "软删除选中的用户"
    
    def activate_users(self, request, queryset):
        """批量激活用户"""
        count = queryset.update(is_active=True, is_deleted=False)
        self.message_user(request, f'成功激活 {count} 个用户。')
    activate_users.short_description = "激活选中的用户"
