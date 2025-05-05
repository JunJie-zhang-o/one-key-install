
from onekeyinstall.installer import Installer
from onekeyinstall.registry import register


@register("feishu")
class InstallFeishu(Installer):

    PACKAGE_NAME = "feishu"

    def install(self):
        return super().install()