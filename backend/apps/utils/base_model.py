from django.db import models
from datetime import datetime


class BaseModel(models.Model):
    """
    基础模型类 - 为所有业务模型提供统一的时间戳字段
    
    包含字段:
    - add_time: 创建时间，自动设置为当前时间
    - update_time: 更新时间，每次保存时自动更新
    """
    add_time = models.DateTimeField(
        default=datetime.now, 
        verbose_name="添加时间",
        help_text="记录创建时间"
    )
    update_time = models.DateTimeField(
        auto_now=True, 
        verbose_name="更新时间",
        help_text="记录最后修改时间"
    )

    class Meta:
        # 抽象基类，不会创建实际的数据库表
        abstract = True
        # 默认按创建时间倒序排列
        ordering = ['-add_time'] 