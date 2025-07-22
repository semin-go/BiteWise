from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager) :
    def create_user(self, email, password = None, **extra_fields) :
        if not email:
            raise ValueError("이메일은 필수입니다.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


# 실제 사용자 모델
class User(AbstractBaseUser, PermissionsMixin) :
    # 성별
    GENDER_CHOICES = [
        ('M', '남자'),
        ('F', '여자'),
    ]

    # 식단
    DIET_PLAN_CHOICES = [
        ('normal', '일반식'),
        ('exercise', '운동'),
    ]

    email = models.EmailField(unique=True)                    # email
    name = models.CharField(max_length=50)                    # 사용자 이름

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)  # 만나이
    height = models.FloatField(null=True, blank=True)         # 키 (cm)
    current_weight = models.FloatField(null=True, blank=True) # 시작 체중 (kg)
    target_weight = models.FloatField(null=True, blank=True)  # 목표 체중 (kg)
    diet_plan = models.CharField(max_length=10, choices=DIET_PLAN_CHOICES, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)             # 활성화
    date_joined = models.DateTimeField(auto_now_add=True)     # 가입일

    objects = UserManager()

    USERNAME_FIELD = 'email'        # 로그인 시 사용할 필드
    REQUIRED_FIELDS = ['name']

    def __str__(self) :
        return self.email