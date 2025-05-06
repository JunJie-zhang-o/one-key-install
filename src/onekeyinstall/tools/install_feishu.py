
from onekeyinstall.installer import Installer
from onekeyinstall.registry import register
from onekeyinstall.utils import Arch, get_offline_install_package_suffix


@register("feishu")
class InstallFeishu(Installer):

    PACKAGE_NAME = "feishu"

# 飞书的带有验证
# https://lf3-ug-sign.feishucdn.com/ee-appcenter/9bcfe8ba/Feishu-linux_x64-7.36.11.deb?lk3s=fb957577&x-expires=1746553895&x-signature=UmNF7PnI%2BqaC6T50KtP6PRp1u84%3D
# https://lf6-ug-sign.feishucdn.com/ee-appcenter/9bcfe8ba/Feishu-linux_x64-7.36.11.rpm?lk3s=fb957577&x-expires=1746554076&x-signature=PTOibsWhggMg827%2BNstftdxXWXQ%3D

# https://lf6-ug-sign.feishucdn.com/ee-appcenter/484fc204/Feishu-linux_arm64-7.36.11.deb?lk3s=fb957577&x-expires=1746554124&x-signature=Rcr3%2F0QJaLAOnyNqw7IoA%2BGYU1Y%3D
# https://lf3-ug-sign.feishucdn.com/ee-appcenter/78243739/Feishu-linux_mips64el-7.22.9.deb?lk3s=fb957577&x-expires=1746554155&x-signature=hj%2B%2BoAmBjoT3VcnRnanQeZ9DPuw%3D
    def pre_install(self):
        url = None




    def install(self):
        return super().install()

