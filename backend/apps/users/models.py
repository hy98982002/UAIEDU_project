from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from apps.utils.base_model import BaseModel


class User(AbstractUser, BaseModel):
    """
    用户模型 - 支持手机号注册登录
    
    继承自Django的AbstractUser和BaseModel
    主要特性:
    - 手机号作为主要登录方式
    - 支持用户资料管理
    - 集成权限控制
    """
    
    # 手机号字段 - 作为唯一标识
    phone_regex = RegexValidator(
        regex=r'^1[3-9]\d{9}$',
        message="请输入有效的手机号码（11位数字，以1开头）"
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=11,
        unique=True,
        verbose_name="手机号",
        help_text="用户注册和登录的手机号码"
    )
    
    # 用户资料字段
    nickname = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="昵称",
        help_text="用户显示昵称"
    )
    
    avatar = models.URLField(
        blank=True,
        null=True,
        verbose_name="头像",
        help_text="用户头像URL地址"
    )
    
    gender_choices = [
        ('M', '男'),
        ('F', '女'),
        ('U', '未知'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=gender_choices,
        default='U',
        verbose_name="性别"
    )
    
    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name="生日"
    )
    
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="个人简介"
    )
    
    # 系统控制字段
    is_deleted = models.BooleanField(
        default=False,
        verbose_name="是否删除",
        help_text="软删除标记，不物理删除用户数据"
    )
    
    # 最后登录IP
    last_login_ip = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name="最后登录IP"
    )

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户管理"
        db_table = "users_user"
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['is_active', 'is_deleted']),
            models.Index(fields=['add_time']),
        ]

    def __str__(self):
        return f"{self.phone} - {self.nickname or self.username}"

    def save(self, *args, **kwargs):
        # 如果没有设置用户名，使用手机号作为用户名
        if not self.username:
            self.username = self.phone
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        """获取用户显示名称"""
        return self.nickname or self.username or self.phone

    def delete(self, using=None, keep_parents=False):
        """重写删除方法，实现软删除"""
        self.is_deleted = True
        self.is_active = False
        self.save()
