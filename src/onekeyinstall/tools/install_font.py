



from onekeyinstall.installer import Installer
from onekeyinstall.registry import register



@register("font.fira-code-nerd-font")
class InstallFiraCodeNerdFont(Installer):
    
    PACKAGE_NAME = "fonts-firacode"

    def register_install(self):        
        self.pm_executor.install(self.PACKAGE_NAME)

    
    def register_uninstall(self):
        self.pm_executor.remove(self.PACKAGE_NAME)




if __name__ == "__main__":

    InstallFiraCodeNerdFont().install()
    InstallFiraCodeNerdFont().uninstall()