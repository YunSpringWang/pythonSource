######################################
# Django 模块
######################################
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
######################################
# 用户扩展表
######################################
class UserInfo(AbstractUser):
    gender_choices = (
        (1, "未知"),
        (2, "男"),
        (3, "女"),
    )

    nickname = models.CharField(verbose_name="昵称", max_length=32, blank=True, null=True)
    # avatar = models.ImageField(verbose_name="头像", upload_to="avatars/", default="/avatars/default.png")
    tel = models.IntegerField(verbose_name="电话", unique=True, blank=True, null=True)
    gender = models.IntegerField(verbose_name="性别", choices=gender_choices, default=1)
    email = models.EmailField('邮箱', unique=True, error_messages={'unique': "该邮箱地址已被占用。", }, )  # 重写auth_user的email
    # departs = models.ForeignKey(to=Depart, on_delete=models.CASCADE, blank=True, null=True)  # 设置外键一定要设置, blank=True, null=True
    c_time = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']