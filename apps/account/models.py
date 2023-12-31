from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import RegexValidator
from apps.common.models import BaseModel


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise TypeError(_('User should have a email'))

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if password is None:
            raise TypeError(_('Password should not be None'))

        user = self.create_user(
            email=email,
            password=password,
            **extra_fields,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, BaseModel, PermissionsMixin):
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    ROLE = (
        (0, 'stuff'),
        (1, 'student'),
        (2, 'teacher'),
    )

    _validate_phone = RegexValidator(
        regex=r"^9\d{12}$",
        message="Telefon raqamingiz 9 bilan boshlanishi va 12 ta belgidan oshmasligi lozim. Masalan: 998993451545", )

    username = models.CharField(max_length=50, unique=True, verbose_name=_('Username'), db_index=True  , null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True, verbose_name=_('Email'), db_index=True)
    full_name = models.CharField(max_length=50, verbose_name=_('Full name'), null=True)
    phone = models.CharField(max_length=16, verbose_name=_('Phone Number'), null=True, validators=[_validate_phone])
    image = models.ImageField(upload_to='accounts/', verbose_name=_('Account image'), null=True, blank=True)
    role = models.IntegerField(choices=ROLE, default=1)
    is_superuser = models.BooleanField(default=False, verbose_name=_('Super user'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Staff user'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active user'))
    date_modified = models.DateTimeField(auto_now=True, verbose_name=_('Date modified'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date created'))

    objects = AccountManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.full_name:
            return f'{self.full_name} ({self.username})'
        return f'{self.email}'

    def image_tag(self):
        if self.image:
            return mark_safe(f'<a href="{self.image.url}"><img src="{self.image.url}" style="height:40px;"/></a>')
        return 'no_image'

    @property
    def image_url(self):
        if self.image:
            if settings.DEBUG:
                return f'{settings.LOCAL_BASE_URL}{self.image.url}'
            return f'{settings.PROD_BASE_URL}{self.image.url}'
        else:
            return None

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data
