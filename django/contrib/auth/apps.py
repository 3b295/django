from django.apps import AppConfig
from django.core import checks
from django.db.models.query_utils import DeferredAttribute
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _

from . import get_user_model
from .checks import check_models_permissions, check_user_model
from .management import create_permissions
from .signals import user_logged_in


class AuthConfig(AppConfig):
    name = 'django.contrib.auth'
    verbose_name = _("Authentication and Authorization")

    def ready(self):
        # 每个app迁移后生成对应的权限表数据
        post_migrate.connect(
            create_permissions,
            dispatch_uid="django.contrib.auth.management.create_permissions"
        )
        last_login_field = getattr(get_user_model(), 'last_login', None)
        # Register the handler only if UserModel.last_login is a field.
        # 通过 DeferredAttribute 来判断是否是数据字段和 db 那边的实现有关
        if isinstance(last_login_field, DeferredAttribute):
            from .models import update_last_login
            # dispatch_uid: 预防接收器被多次注册，唯一的 dispatch_uid 仅被绑定一次
            user_logged_in.connect(update_last_login, dispatch_uid='update_last_login')

        # 对 user model 和 permissions model 进行静态检查，在大多数命令前隐式执行（不包括 WSGI 部署)
        checks.register(check_user_model, checks.Tags.models)
        checks.register(check_models_permissions, checks.Tags.models)
