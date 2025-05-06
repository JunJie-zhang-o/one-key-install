
from onekeyinstall.installer import Installer
from onekeyinstall.registry import register
from onekeyinstall.utils import Arch, get_offline_install_package_suffix


@register("weichat")
class InstallWeichat(Installer):

    PACKAGE_NAME = "weichat"


    def pre_install(self):
        url = None
        offline_package_suffix = get_offline_install_package_suffix()
        if self._system.arch == Arch.X86:
            _arch = "X86_64"
        elif self._system.arch == Arch.ARM:
            _arch = "arm64"
        elif self._system.arch == Arch.LOONGARCH:
            _arch = "LoongArch"
        else:
            return False
        
        if "deb" in offline_package_suffix:
            _suffix = "deb"
        elif "rpm" in offline_package_suffix:
            _suffix = "rpm"
        else:
            return False

        url = f"https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_{_arch}.{_suffix}"
        self.offline_package = self.downloader.download(url, f"WeChatLinux.{_suffix}")


    def install(self):
        self.pm_executor.install(self.offline_package)