


from onekeyinstall.installer import Installer
from onekeyinstall.registry import register


@register("terminal.btop")
class InstallBtop(Installer):

    PACKAGE_NAME = "btop"


    def register_install(self):
        return super().register_install()
    
    def register_uninstall(self):
        return super().register_uninstall()

    def description(self):
        md = """
            # Btop 是一个终端工具 
        """
        return  md


@register("terminal.htop")
class InstallHtop(Installer):

    PACKAGE_NAME = "htop"


    def register_install(self):
        return super().register_install()
    
    def register_uninstall(self):
        return super().register_uninstall()

    def description(self):
        md = """
            # InstallHtop 是一个终端工具 
        """
        return  md

@register("terminal.nvitop")
class InstallNvitop(Installer):

    PACKAGE_NAME = "nvitop"


    def register_install(self):
        self._install.add(f"pip3 install {self.PACKAGE_NAME}", lambda: self._executor.run(f"pip3 install {self.PACKAGE_NAME} -i https://pypi.tuna.tsinghua.edu.cn/simple"))


    def register_uninstall(self):
        self._uninstall.add(f"pip3 uninstall {self.PACKAGE_NAME}", lambda:self._executor.run(f"pip3 uninstall {self.PACKAGE_NAME}"))
        

    def description(self):
        md = """
            # InstallNvitop 是一个终端工具 
        """
        return  md