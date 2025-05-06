


from onekeyinstall.installer import Installer
from onekeyinstall.registry import register


@register("terminal.btop")
class InstallBtop(Installer):

    PACKAGE_NAME = "btop"



@register("terminal.htop")
class InstallHtop(Installer):

    PACKAGE_NAME = "htop"

    

@register("terminal.nvitop")
class InstallNvitop(Installer):

    PACKAGE_NAME = "nvitop"

    def install(self):
        # return super().install()
        self._executor.run(f"pip3 install {self.PACKAGE_NAME} -i https://pypi.tuna.tsinghua.edu.cn/simple")

    
    def remove(self):
        self._executor.run(f"pip3 uninstall {self.PACKAGE_NAME}")
        