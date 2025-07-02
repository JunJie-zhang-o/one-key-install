


from onekeyinstall.installer import Installer
from onekeyinstall.registry import register
from onekeyinstall.utils import Arch, get_offline_install_package_suffix


class InstallSnipaste(Installer):


    def register_install(self):
        return super().register_install()
    


    def register_uninstall(self):
        return super().register_uninstall()
